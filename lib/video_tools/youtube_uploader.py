#!/usr/bin/env python3
"""
YouTube Upload API Setup and Implementation
Handles video uploads with playlist assignment and metadata
"""

import os
import sys
import json
import pickle
from typing import Dict, Optional, List
from pathlib import Path

import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

class YouTubeUploader:
    """Handles YouTube video uploads with playlist management"""
    
    # YouTube API scopes - using only what Google grants
    # Note: youtube.force-ssl includes upload capabilities
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.force-ssl'
    ]
    
    def __init__(self):
        load_dotenv()
        self.service = None
        self.credentials_file = 'config/youtube_credentials.json'
        self.token_file = 'config/youtube_token.pickle'
        
        # Load playlist IDs from environment
        self.playlists = {
            'en': os.getenv('GUIDORA_ENGLISH_PLAYLIST'),
            'es': os.getenv('GUIDORA_SPANISH_PLAYLIST'), 
            'fr': os.getenv('GUIDORA_FRENCH_PLAYLIST'),
            'ur': os.getenv('GUIDORA_HINDI_AND_URDU_PLAYLIST')  # Note: says Hindi and Urdu
        }
        
        # Ensure config directory exists
        os.makedirs('config', exist_ok=True)
        
    def authenticate(self) -> bool:
        """Authenticate with YouTube API"""
        
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"❌ Error refreshing token: {e}")
                    return False
            else:
                if not os.path.exists(self.credentials_file):
                    print(f"❌ YouTube credentials file not found: {self.credentials_file}")
                    print("📋 Please follow setup instructions to get credentials")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                # Try different authentication methods
                try:
                    print("🔄 Trying local server on port 8080...")
                    creds = flow.run_local_server(port=8080, open_browser=True)
                except Exception as e:
                    print(f"⚠️ Port 8080 failed: {str(e)[:100]}...")
                    try:
                        print("🔄 Trying local server on port 8090...")
                        creds = flow.run_local_server(port=8090, open_browser=True)
                    except Exception as e2:
                        print(f"⚠️ Port 8090 failed: {str(e2)[:100]}...")
                        print("🔄 Using manual authorization flow...")
                        # Use manual flow - user copies URL and pastes code
                        auth_url, _ = flow.authorization_url(prompt='consent')
                        print(f"\n📋 MANUAL AUTHORIZATION REQUIRED:")
                        print(f"1. Visit this URL: {auth_url}")
                        print(f"2. Sign in and authorize the application")
                        print(f"3. Copy the authorization code")
                        code = input("4. Paste the authorization code here: ").strip()
                        flow.fetch_token(code=code)
                        creds = flow.credentials
            
            # Save credentials for next time
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        # Build the service
        try:
            self.service = build('youtube', 'v3', credentials=creds)
            print("✅ YouTube API authenticated successfully")
            return True
        except Exception as e:
            print(f"❌ Error building YouTube service: {e}")
            return False
    
    def upload_video(self, video_path: str, metadata: Dict, language: str = 'en') -> Optional[str]:
        """Upload video to YouTube with metadata and playlist assignment"""
        
        if not self.service:
            print("❌ YouTube service not authenticated")
            return None
        
        if not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return None
        
        try:
            print(f"🔄 Uploading video: {os.path.basename(video_path)}")
            print(f"🌍 Language: {language.upper()}")
            print(f"📝 Title: {metadata.get('title', 'Untitled')}")
            
            # Prepare video metadata
            body = {
                'snippet': {
                    'title': metadata.get('title', 'Untitled Video'),
                    'description': metadata.get('description', ''),
                    'tags': metadata.get('tags', []),
                    'categoryId': metadata.get('category_id', '22'),  # People & Blogs
                    'defaultLanguage': language,
                    'defaultAudioLanguage': language
                },
                'status': {
                    'privacyStatus': metadata.get('privacy', 'private'),  # Start as private
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Prepare video file for upload
            media = MediaFileUpload(
                video_path,
                chunksize=-1,
                resumable=True,
                mimetype='video/mp4'
            )
            
            # Execute upload
            upload_request = self.service.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            video_id = self._execute_upload(upload_request)
            
            if video_id:
                print(f"✅ Video uploaded successfully: {video_id}")
                
                # Add to playlist if specified
                playlist_id = self.playlists.get(language)
                if playlist_id:
                    if self.add_to_playlist(video_id, playlist_id):
                        print(f"✅ Added to {language.upper()} playlist: {playlist_id}")
                    else:
                        print(f"⚠️ Failed to add to playlist")
                
                # Set thumbnail if provided
                thumbnail_path = metadata.get('thumbnail_path')
                if thumbnail_path and os.path.exists(thumbnail_path):
                    if self.set_thumbnail(video_id, thumbnail_path):
                        print(f"✅ Thumbnail uploaded successfully")
                    else:
                        print(f"⚠️ Failed to upload thumbnail")
                
                return video_id
            else:
                print("❌ Upload failed")
                return None
                
        except HttpError as e:
            print(f"❌ HTTP Error during upload: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error during upload: {e}")
            return None
    
    def _execute_upload(self, upload_request) -> Optional[str]:
        """Execute the actual upload with progress tracking"""
        
        response = None
        error = None
        retry = 0
        
        while response is None:
            try:
                print(f"🔄 Upload attempt {retry + 1}")
                status, response = upload_request.next_chunk()
                
                if status:
                    progress = int(status.progress() * 100)
                    print(f"📊 Upload progress: {progress}%")
                    
            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    error = f"Server error: {e}"
                    retry += 1
                    if retry > 3:
                        print(f"❌ Max retries exceeded: {error}")
                        return None
                else:
                    print(f"❌ HTTP Error: {e}")
                    return None
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                return None
        
        if 'id' in response:
            return response['id']
        else:
            print(f"❌ Upload failed: {response}")
            return None
    
    def add_to_playlist(self, video_id: str, playlist_id: str) -> bool:
        """Add video to specified playlist"""
        
        try:
            playlist_item = {
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
            
            self.service.playlistItems().insert(
                part='snippet',
                body=playlist_item
            ).execute()
            
            return True
            
        except HttpError as e:
            print(f"❌ Error adding to playlist: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error adding to playlist: {e}")
            return False
    
    def set_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """Set custom thumbnail for video"""
        
        try:
            self.service.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            ).execute()
            
            return True
            
        except HttpError as e:
            print(f"❌ Error setting thumbnail: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error setting thumbnail: {e}")
            return False
    
    def check_playlists(self) -> Dict:
        """Verify playlist IDs are valid and accessible"""
        
        if not self.service:
            return {"error": "Not authenticated"}
        
        results = {}
        
        for lang, playlist_id in self.playlists.items():
            if not playlist_id:
                results[lang] = {"status": "missing", "id": None}
                continue
            
            try:
                # Try to fetch playlist details
                response = self.service.playlists().list(
                    part='snippet',
                    id=playlist_id
                ).execute()
                
                if response['items']:
                    playlist = response['items'][0]
                    results[lang] = {
                        "status": "valid",
                        "id": playlist_id,
                        "title": playlist['snippet']['title'],
                        "description": playlist['snippet']['description']
                    }
                else:
                    results[lang] = {"status": "not_found", "id": playlist_id}
                    
            except HttpError as e:
                results[lang] = {"status": "error", "id": playlist_id, "error": str(e)}
            except Exception as e:
                results[lang] = {"status": "error", "id": playlist_id, "error": str(e)}
        
        return results

def setup_youtube_credentials():
    """Guide user through YouTube API setup"""
    
    print("🎯 YOUTUBE API SETUP GUIDE")
    print("=" * 50)
    
    print("\n📋 Steps to set up YouTube API:")
    print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Enable YouTube Data API v3")
    print("4. Create credentials (OAuth 2.0 Client IDs)")
    print("5. Download credentials JSON file")
    print("6. Save as: config/youtube_credentials.json")
    
    print(f"\n📁 Required file location:")
    print(f"   {os.path.abspath('config/youtube_credentials.json')}")
    
    print(f"\n✅ Playlist IDs already configured:")
    load_dotenv()
    playlists = {
        'en': os.getenv('GUIDORA_ENGLISH_PLAYLIST'),
        'es': os.getenv('GUIDORA_SPANISH_PLAYLIST'), 
        'fr': os.getenv('GUIDORA_FRENCH_PLAYLIST'),
        'ur': os.getenv('GUIDORA_HINDI_AND_URDU_PLAYLIST')
    }
    
    for lang, playlist_id in playlists.items():
        print(f"   {lang.upper()}: {playlist_id}")
    
    print(f"\n🔗 Useful links:")
    print(f"   Google Cloud Console: https://console.cloud.google.com/")
    print(f"   YouTube API Guide: https://developers.google.com/youtube/v3/getting-started")

def main():
    """Test YouTube uploader setup"""
    
    print("🎯 YOUTUBE UPLOADER SETUP TEST")
    print("=" * 40)
    
    # Check if credentials file exists
    creds_file = 'config/youtube_credentials.json'
    if not os.path.exists(creds_file):
        print(f"❌ Credentials file not found: {creds_file}")
        setup_youtube_credentials()
        return
    
    # Initialize uploader
    uploader = YouTubeUploader()
    
    # Test authentication
    if uploader.authenticate():
        print("✅ YouTube API authentication successful!")
        
        # Check playlists
        print("\n📋 Checking playlist accessibility...")
        playlist_results = uploader.check_playlists()
        
        for lang, result in playlist_results.items():
            status = result['status']
            if status == 'valid':
                print(f"✅ {lang.upper()}: {result['title']}")
            elif status == 'missing':
                print(f"❌ {lang.upper()}: No playlist ID configured")
            elif status == 'not_found':
                print(f"❌ {lang.upper()}: Playlist not found - {result['id']}")
            else:
                print(f"❌ {lang.upper()}: Error - {result.get('error', 'Unknown error')}")
        
        print("\n🚀 YouTube uploader is ready for production!")
        
    else:
        print("❌ YouTube API authentication failed")
        setup_youtube_credentials()

if __name__ == "__main__":
    main()
