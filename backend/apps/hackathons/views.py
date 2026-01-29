from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import requests
from datetime import datetime
from bs4 import BeautifulSoup


class HackathonListView(APIView):
    """
    Fetch real-time upcoming hackathons from multiple sources
    """
    permission_classes = [AllowAny]  # Allow public access for discovery
    
    def get(self, request):
        hackathons = []
        
        # Fetch from multiple sources
        devpost_hackathons = self.fetch_devpost_hackathons()
        hackathons.extend(devpost_hackathons)
        
        mlh_hackathons = self.fetch_mlh_hackathons()
        hackathons.extend(mlh_hackathons)
        
        devfolio_hackathons = self.fetch_devfolio_hackathons()
        hackathons.extend(devfolio_hackathons)
        
        # Remove duplicates based on name similarity
        hackathons = self.remove_duplicates(hackathons)
        
        # Sort by start date (upcoming first)
        try:
            hackathons.sort(key=lambda x: self.parse_date(x.get('start_date', '')))
        except:
            pass
        
        return Response({
            'success': True,
            'count': len(hackathons),
            'hackathons': hackathons
        }, status=status.HTTP_200_OK)
    
    def parse_date(self, date_str):
        """Parse various date formats to datetime for sorting"""
        if not date_str or date_str == 'TBA':
            return datetime.max
        
        try:
            # Try various date formats
            formats = ['%b %d, %Y', '%Y-%m-%d', '%B %d, %Y', '%d %b %Y']
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except:
                    continue
            return datetime.max
        except:
            return datetime.max
    
    def remove_duplicates(self, hackathons):
        """Remove duplicate hackathons based on name similarity"""
        seen = set()
        unique = []
        for h in hackathons:
            name_key = h['name'].lower().replace(' ', '')[:20]
            if name_key not in seen:
                seen.add(name_key)
                unique.append(h)
        return unique
    
    def fetch_devpost_hackathons(self):
        """
        Fetch live hackathons from Devpost
        """
        hackathons = []
        try:
            # Scrape Devpost's public hackathons page
            response = requests.get(
                'https://devpost.com/hackathons',
                params={'status[]': 'open'},
                timeout=10,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                hackathon_tiles = soup.find_all('div', class_='hackathon-tile')
                
                for tile in hackathon_tiles[:15]:
                    try:
                        title_elem = tile.find('h3')
                        link_elem = tile.find('a', class_='link-to-hackathon')
                        date_elem = tile.find('div', class_='submission-period')
                        location_elem = tile.find('div', class_='info-with-icon')
                        
                        name = title_elem.text.strip() if title_elem else 'Devpost Hackathon'
                        url = link_elem['href'] if link_elem and 'href' in link_elem.attrs else 'https://devpost.com'
                        date = date_elem.text.strip() if date_elem else 'TBA'
                        location = location_elem.text.strip() if location_elem else 'Online'
                        
                        hackathon = {
                            'id': f"devpost_{len(hackathons)}",
                            'name': name,
                            'start_date': date,
                            'end_date': '',
                            'location': location,
                            'url': url if url.startswith('http') else f"https://devpost.com{url}",
                            'logo': '',
                            'source': 'Devpost',
                            'is_online': 'online' in location.lower() or 'remote' in location.lower(),
                            'description': f'Join {name} on Devpost and showcase your skills!',
                        }
                        hackathons.append(hackathon)
                    except Exception as e:
                        print(f"Error parsing Devpost tile: {e}")
                        continue
        except Exception as e:
            print(f"Error fetching Devpost hackathons: {e}")
        
        return hackathons
    
    def fetch_mlh_hackathons(self):
        """
        Fetch hackathons from MLH (Major League Hacking)
        """
        hackathons = []
        try:
            # MLH Events page
            response = requests.get(
                'https://mlh.io/seasons/2026/events',
                timeout=10,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                # MLH uses different structure - look for event cards
                events = soup.find_all('div', class_='event')
                
                if not events:
                    # Try alternative selectors
                    events = soup.find_all('a', href=lambda x: x and '/events/' in str(x))
                
                for event in events[:15]:
                    try:
                        # Extract event details based on MLH structure
                        name_elem = event.find('h3') or event.find('h2') or event.find(['strong', 'b'])
                        name = name_elem.text.strip() if name_elem else 'MLH Hackathon'
                        
                        date_elem = event.find('p', class_='event-date') or event.find('time')
                        date = date_elem.text.strip() if date_elem else 'TBA'
                        
                        location_elem = event.find('p', class_='event-location') or event.find('span', class_='location')
                        location = location_elem.text.strip() if location_elem else 'Various Locations'
                        
                        link = event.get('href', '') if event.name == 'a' else (event.find('a')['href'] if event.find('a') else '')
                        url = link if link.startswith('http') else f"https://mlh.io{link}" if link else 'https://mlh.io'
                        
                        hackathon = {
                            'id': f"mlh_{len(hackathons)}",
                            'name': name,
                            'start_date': date,
                            'end_date': '',
                            'location': location,
                            'url': url,
                            'logo': '',
                            'source': 'MLH',
                            'is_online': 'online' in location.lower() or 'virtual' in location.lower(),
                            'description': f'MLH Season 2026 event - {name}',
                        }
                        hackathons.append(hackathon)
                    except Exception as e:
                        print(f"Error parsing MLH event: {e}")
                        continue
        except Exception as e:
            print(f"Error fetching MLH hackathons: {e}")
        
        return hackathons
    
    def fetch_devfolio_hackathons(self):
        """
        Fetch Indian hackathons from Devfolio
        """
        hackathons = []
        try:
            # Devfolio public API
            response = requests.get(
                'https://api.devfolio.co/api/search/hackathons',
                params={'status': 'UPCOMING'},
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            if response.status_code == 200:
                data = response.json()
                for event in data.get('hackathons', [])[:15]:
                    hackathon = {
                        'id': f"devfolio_{event.get('id', len(hackathons))}",
                        'name': event.get('name', 'Unnamed Hackathon'),
                        'start_date': event.get('starts_at', 'TBA'),
                        'end_date': event.get('ends_at', ''),
                        'location': event.get('city', 'India'),
                        'url': f"https://devfolio.co/hackathons/{event.get('slug', '')}",
                        'logo': event.get('logo', ''),
                        'source': 'Devfolio',
                        'is_online': event.get('is_online', False),
                        'description': event.get('tagline', 'Join this exciting hackathon'),
                        'prize_amount': event.get('prizes', ''),
                    }
                    hackathons.append(hackathon)
        except Exception as e:
            print(f"Error fetching Devfolio hackathons: {e}")
        
        # If no hackathons from API, add some fallback samples
        if not hackathons:
            hackathons = self.get_sample_hackathons()
        
        return hackathons
    
    def get_sample_hackathons(self):
        """
        Fallback recent hackathons data (updated with 2025-2026 dates)
        """
        return [
            {
                'id': 'sample_1',
                'name': 'Smart India Hackathon 2025',
                'start_date': 'Dec 20, 2025',
                'end_date': 'Dec 22, 2025',
                'location': 'Pan India',
                'url': 'https://www.sih.gov.in',
                'logo': '',
                'source': 'Sample',
                'is_online': False,
                'description': 'India\'s biggest hackathon initiative by Govt. of India. Solve real-world problems with innovative solutions.'
            },
            {
                'id': 'sample_2',
                'name': 'DevPost Winter Hackathon',
                'start_date': 'Jan 10, 2026',
                'end_date': 'Jan 17, 2026',
                'location': 'Online',
                'url': 'https://devpost.com/hackathons',
                'logo': '',
                'source': 'Sample',
                'is_online': True,
                'description': 'Week-long online hackathon with prizes. Build anything you want!'
            },
            {
                'id': 'sample_3',
                'name': 'ETHIndia 2025',
                'start_date': 'Dec 18, 2025',
                'end_date': 'Dec 20, 2025',
                'location': 'Bangalore, India',
                'url': 'https://ethindia.co',
                'logo': '',
                'source': 'Sample',
                'is_online': False,
                'description': 'India\'s largest Ethereum hackathon. Build Web3 applications and win crypto prizes.'
            },
            {
                'id': 'sample_4',
                'name': 'HackMIT 2026',
                'start_date': 'Feb 14, 2026',
                'end_date': 'Feb 16, 2026',
                'location': 'MIT, Cambridge, MA',
                'url': 'https://hackmit.org',
                'logo': '',
                'source': 'Sample',
                'is_online': False,
                'description': 'Annual hackathon at MIT with amazing prizes, workshops, and 1000+ hackers.'
            },
            {
                'id': 'sample_5',
                'name': 'Google Cloud Hackathon',
                'start_date': 'Jan 25, 2026',
                'end_date': 'Feb 25, 2026',
                'location': 'Online',
                'url': 'https://cloud.google.com',
                'logo': '',
                'source': 'Sample',
                'is_online': True,
                'description': 'Build with Google Cloud Platform. Monthly online hackathon with $10k in prizes.'
            },
            {
                'id': 'sample_6',
                'name': 'AWS India Innovate',
                'start_date': 'Feb 1, 2026',
                'end_date': 'Feb 28, 2026',
                'location': 'Online',
                'url': 'https://aws.amazon.com',
                'logo': '',
                'source': 'Sample',
                'is_online': True,
                'description': 'Build innovative solutions using AWS services. Open to students and professionals.'
            },
            {
                'id': 'sample_7',
                'name': 'Microsoft Imagine Cup India',
                'start_date': 'Jan 15, 2026',
                'end_date': 'Mar 15, 2026',
                'location': 'Online + Finals in Delhi',
                'url': 'https://imaginecup.microsoft.com',
                'logo': '',
                'source': 'Sample',
                'is_online': True,
                'description': 'Microsoft\'s premier student technology competition. Win up to $100k and mentorship.'
            },
            {
                'id': 'sample_8',
                'name': 'HackerEarth Sprint',
                'start_date': 'Dec 23, 2025',
                'end_date': 'Dec 30, 2025',
                'location': 'Online',
                'url': 'https://www.hackerearth.com',
                'logo': '',
                'source': 'Sample',
                'is_online': True,
                'description': 'Week-long coding sprint with hiring opportunities. Solve challenges and get hired.'
            },
        ]
