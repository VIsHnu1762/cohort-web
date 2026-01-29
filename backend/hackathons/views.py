from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import requests
from datetime import datetime


class HackathonListView(APIView):
    """
    API endpoint to fetch and return hackathon listings
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Fetch hackathons from external APIs and return the list
        """
        try:
            # Try to fetch from external API
            hackathons = self.fetch_devpost_hackathons()
            
            # Sort by start date
            hackathons.sort(key=lambda x: x.get('start_date', ''), reverse=False)
            
            return Response({
                'success': True,
                'count': len(hackathons),
                'hackathons': hackathons
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def fetch_devpost_hackathons(self):
        """
        Fetch hackathons from multiple sources using real APIs and web scraping
        """
        all_hackathons = []
        
        # Try MLH (Major League Hacking) - They have a public events page
        try:
            response = requests.get(
                'https://mlh.io/seasons/2025/events',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/json'
                },
                timeout=10
            )
            if response.status_code == 200:
                # Try to parse if JSON, otherwise we got HTML
                try:
                    data = response.json()
                    for item in data[:15]:
                        all_hackathons.append({
                            'id': f"mlh_{item.get('id', '')}",
                            'name': item.get('name', 'MLH Hackathon'),
                            'start_date': item.get('start_date', 'TBA'),
                            'end_date': item.get('end_date', 'TBA'),
                            'location': item.get('location', 'Various'),
                            'url': item.get('url', 'https://mlh.io'),
                            'logo': item.get('image_url', item.get('logo', 'https://via.placeholder.com/300x150?text=MLH')),
                            'source': 'MLH',
                            'is_online': 'digital' in str(item.get('location', '')).lower() or 'online' in str(item.get('location', '')).lower(),
                            'description': item.get('description', 'Official MLH Member Event')[:200]
                        })
                    print(f"Fetched {len(all_hackathons)} hackathons from MLH API")
                except:
                    # HTML response - try to extract data
                    import re
                    # Look for JSON data embedded in script tags
                    json_match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', response.text, re.DOTALL)
                    if json_match:
                        import json
                        data = json.loads(json_match.group(1))
                        events = data.get('events', [])
                        for item in events[:15]:
                            all_hackathons.append({
                                'id': f"mlh_{item.get('id', '')}",
                                'name': item.get('name', 'MLH Hackathon'),
                                'start_date': item.get('start_date', 'TBA'),
                                'end_date': item.get('end_date', 'TBA'),
                                'location': item.get('location', 'Various'),
                                'url': item.get('url', 'https://mlh.io'),
                                'logo': item.get('image_url', 'https://via.placeholder.com/300x150?text=MLH'),
                                'source': 'MLH',
                                'is_online': 'digital' in str(item.get('location', '')).lower(),
                                'description': 'Official MLH Member Event'[:200]
                            })
                        print(f"Fetched {len(all_hackathons)} hackathons from MLH HTML")
        except Exception as e:
            print(f"MLH error: {e}")
        
        # Try DevPost - Scrape their hackathons page
        try:
            response = requests.get(
                'https://devpost.com/hackathons',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html'
                },
                timeout=10
            )
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find hackathon cards
                hackathon_cards = soup.find_all('div', class_='challenge-listing', limit=15)
                count_before = len(all_hackathons)
                
                for card in hackathon_cards:
                    try:
                        title_elem = card.find('h3') or card.find('h2') or card.find(class_='title')
                        title = title_elem.get_text(strip=True) if title_elem else 'DevPost Hackathon'
                        
                        link_elem = card.find('a', href=True)
                        url = f"https://devpost.com{link_elem['href']}" if link_elem and link_elem['href'].startswith('/') else link_elem['href'] if link_elem else 'https://devpost.com'
                        
                        img_elem = card.find('img')
                        logo = img_elem['src'] if img_elem and 'src' in img_elem.attrs else 'https://via.placeholder.com/300x150?text=DevPost'
                        
                        desc_elem = card.find('p') or card.find(class_='description')
                        description = desc_elem.get_text(strip=True)[:200] if desc_elem else 'Join this DevPost hackathon'
                        
                        date_elem = card.find(class_='date') or card.find(string=re.compile(r'\d+'))
                        date_text = date_elem.get_text(strip=True) if date_elem else 'TBA'
                        
                        all_hackathons.append({
                            'id': f"devpost_{abs(hash(title))}",
                            'name': title,
                            'start_date': date_text,
                            'end_date': date_text,
                            'location': 'Online',
                            'url': url,
                            'logo': logo,
                            'source': 'DevPost',
                            'is_online': True,
                            'description': description
                        })
                    except Exception as e:
                        print(f"Error parsing DevPost card: {e}")
                        continue
                
                print(f"Fetched {len(all_hackathons) - count_before} hackathons from DevPost")
        except ImportError:
            print("BeautifulSoup not installed. Install with: pip install beautifulsoup4")
        except Exception as e:
            print(f"DevPost error: {e}")
        
        # Try Unstop with proper headers
        try:
            response = requests.get(
                'https://unstop.com/hackathons',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html'
                },
                timeout=10
            )
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try to find hackathon cards (adjust selectors based on actual page structure)
                count_before = len(all_hackathons)
                cards = soup.find_all(['div', 'article'], class_=re.compile(r'card|opportunity|hackathon'), limit=10)
                
                for card in cards:
                    try:
                        title = card.find(['h2', 'h3', 'h4'])
                        if not title:
                            continue
                        
                        name = title.get_text(strip=True)
                        link = card.find('a', href=True)
                        url = f"https://unstop.com{link['href']}" if link and link['href'].startswith('/') else link['href'] if link else 'https://unstop.com'
                        
                        all_hackathons.append({
                            'id': f"unstop_{abs(hash(name))}",
                            'name': name,
                            'start_date': 'Check Unstop',
                            'end_date': 'Check Unstop',
                            'location': 'India',
                            'url': url,
                            'logo': 'https://via.placeholder.com/300x150?text=Unstop',
                            'source': 'Unstop',
                            'is_online': False,
                            'description': 'Participate in this Unstop hackathon'
                        })
                    except:
                        continue
                
                print(f"Fetched {len(all_hackathons) - count_before} hackathons from Unstop")
        except ImportError:
            pass
        except Exception as e:
            print(f"Unstop error: {e}")
        
        # If we got real data, return it
        if all_hackathons:
            print(f"Total real hackathons: {len(all_hackathons)}")
            return all_hackathons
        
        # Fallback to sample data
        print("All APIs failed, using sample data")
        return self.get_sample_hackathons()
        return self.get_sample_hackathons()
    
    def get_sample_hackathons(self):
        """
        Return sample hackathon data with current and upcoming dates as fallback
        Based on real hackathon platforms and actual events
        """
        from datetime import datetime, timedelta
        today = datetime.now()
        
        return [
            # Upcoming hackathons from various platforms
            {
                'id': 'sample_1',
                'name': 'Google AI Hackathon 2025',
                'start_date': (today + timedelta(days=10)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=12)).strftime('%b %d, %Y'),
                'location': 'Mountain View, CA',
                'url': 'https://developers.google.com/community/events',
                'logo': 'https://via.placeholder.com/300x150?text=Google+AI',
                'source': 'Sample',
                'is_online': False,
                'description': 'Build the next generation of AI-powered applications using Google Cloud AI and ML tools. $50K in prizes.'
            },
            {
                'id': 'sample_2',
                'name': 'ETHGlobal London',
                'start_date': (today + timedelta(days=18)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=20)).strftime('%b %d, %Y'),
                'location': 'London, UK',
                'url': 'https://ethglobal.com',
                'logo': 'https://via.placeholder.com/300x150?text=ETHGlobal',
                'source': 'Sample',
                'is_online': False,
                'description': 'Build decentralized applications on Ethereum. Connect with 500+ developers from across Europe.'
            },
            {
                'id': 'sample_3',
                'name': 'Microsoft Imagine Cup',
                'start_date': (today + timedelta(days=25)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=27)).strftime('%b %d, %Y'),
                'location': 'Online',
                'url': 'https://imaginecup.microsoft.com',
                'logo': 'https://via.placeholder.com/300x150?text=Imagine+Cup',
                'source': 'Sample',
                'is_online': True,
                'description': 'Global student technology competition. Solve real-world problems using Azure and Microsoft technologies.'
            },
            {
                'id': 'sample_4',
                'name': 'NASA Space Apps Challenge',
                'start_date': (today + timedelta(days=30)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=32)).strftime('%b %d, %Y'),
                'location': 'Global - Multiple Cities',
                'url': 'https://www.spaceappschallenge.org',
                'logo': 'https://via.placeholder.com/300x150?text=NASA+Space+Apps',
                'source': 'Sample',
                'is_online': True,
                'description': 'International hackathon using NASA data. Solve challenges related to Earth and space exploration.'
            },
            {
                'id': 'sample_5',
                'name': 'HackMIT 2025',
                'start_date': (today + timedelta(days=35)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=37)).strftime('%b %d, %Y'),
                'location': 'MIT, Cambridge, MA',
                'url': 'https://hackmit.org',
                'logo': 'https://via.placeholder.com/300x150?text=HackMIT',
                'source': 'Sample',
                'is_online': False,
                'description': 'MIT\'s premier hackathon. 36 hours of hacking with top tech companies and cutting-edge APIs.'
            },
            {
                'id': 'sample_6',
                'name': 'Amazon AWS DeepRacer',
                'start_date': (today + timedelta(days=40)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=42)).strftime('%b %d, %Y'),
                'location': 'Online',
                'url': 'https://aws.amazon.com/deepracer',
                'logo': 'https://via.placeholder.com/300x150?text=AWS+DeepRacer',
                'source': 'Sample',
                'is_online': True,
                'description': 'Machine learning racing competition. Train reinforcement learning models and compete globally.'
            },
            {
                'id': 'sample_7',
                'name': 'Meta AR/VR Hackathon',
                'start_date': (today + timedelta(days=45)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=47)).strftime('%b %d, %Y'),
                'location': 'Menlo Park, CA',
                'url': 'https://about.meta.com',
                'logo': 'https://via.placeholder.com/300x150?text=Meta+AR+VR',
                'source': 'Sample',
                'is_online': False,
                'description': 'Build immersive experiences using Meta Quest and AR technologies. $100K prize pool.'
            },
            {
                'id': 'sample_8',
                'name': 'Unstop Tech Week Hackathon',
                'start_date': (today + timedelta(days=50)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=52)).strftime('%b %d, %Y'),
                'location': 'Bangalore, India',
                'url': 'https://unstop.com',
                'logo': 'https://via.placeholder.com/300x150?text=Unstop+Tech',
                'source': 'Sample',
                'is_online': False,
                'description': 'India\'s largest tech hackathon. Solve challenges from top companies like Flipkart, Swiggy, and Razorpay.'
            },
            {
                'id': 'sample_9',
                'name': 'Y Combinator Startup Weekend',
                'start_date': (today + timedelta(days=55)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=57)).strftime('%b %d, %Y'),
                'location': 'San Francisco, CA',
                'url': 'https://www.ycombinator.com',
                'logo': 'https://via.placeholder.com/300x150?text=YC+Weekend',
                'source': 'Sample',
                'is_online': False,
                'description': 'Build a startup in 54 hours. Pitch to YC partners and get a chance for seed funding.'
            },
            {
                'id': 'sample_10',
                'name': 'OpenAI GPT-4 Challenge',
                'start_date': (today + timedelta(days=60)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=62)).strftime('%b %d, %Y'),
                'location': 'Online',
                'url': 'https://openai.com',
                'logo': 'https://via.placeholder.com/300x150?text=OpenAI',
                'source': 'Sample',
                'is_online': True,
                'description': 'Create innovative applications using GPT-4 and DALL-E 3. Win OpenAI API credits and recognition.'
            },
            {
                'id': 'sample_11',
                'name': 'Stanford TreeHacks',
                'start_date': (today + timedelta(days=65)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=67)).strftime('%b %d, %Y'),
                'location': 'Stanford University, CA',
                'url': 'https://www.treehacks.com',
                'logo': 'https://via.placeholder.com/300x150?text=TreeHacks',
                'source': 'Sample',
                'is_online': False,
                'description': 'Stanford\'s hackathon focused on social impact. Build tech solutions that make the world better.'
            },
            {
                'id': 'sample_12',
                'name': 'Devfolio India Hackathon Series',
                'start_date': (today + timedelta(days=70)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=72)).strftime('%b %d, %Y'),
                'location': 'Mumbai, India',
                'url': 'https://devfolio.co',
                'logo': 'https://via.placeholder.com/300x150?text=Devfolio',
                'source': 'Sample',
                'is_online': False,
                'description': 'Premier hackathon for Indian developers. Network with tech leaders and win internships at top startups.'
            },
            {
                'id': 'sample_13',
                'name': 'GitHub Arctic Code Vault',
                'start_date': (today + timedelta(days=75)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=90)).strftime('%b %d, %Y'),
                'location': 'Online',
                'url': 'https://github.com',
                'logo': 'https://via.placeholder.com/300x150?text=GitHub',
                'source': 'Sample',
                'is_online': True,
                'description': 'Month-long coding challenge. Contribute to open source and get featured in GitHub\'s highlights.'
            },
            {
                'id': 'sample_14',
                'name': 'Hack2Skill IoT Challenge',
                'start_date': (today + timedelta(days=80)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=82)).strftime('%b %d, %Y'),
                'location': 'Online',
                'url': 'https://hack2skill.com',
                'logo': 'https://via.placeholder.com/300x150?text=Hack2Skill',
                'source': 'Sample',
                'is_online': True,
                'description': 'Build IoT solutions for smart homes and cities. Hardware kits provided to top 50 teams.'
            },
            {
                'id': 'sample_15',
                'name': 'TechCrunch Disrupt Hackathon',
                'start_date': (today + timedelta(days=85)).strftime('%b %d, %Y'),
                'end_date': (today + timedelta(days=87)).strftime('%b %d, %Y'),
                'location': 'San Francisco, CA',
                'url': 'https://techcrunch.com/events',
                'logo': 'https://via.placeholder.com/300x150?text=TechCrunch',
                'source': 'Sample',
                'is_online': False,
                'description': 'Present your hack on TechCrunch Disrupt stage. Exposure to thousands of attendees and investors.'
            }
        ]
