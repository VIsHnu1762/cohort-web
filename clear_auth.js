// Run this in your browser console (F12 -> Console tab) to clear everything

// Clear all localStorage
localStorage.clear();

// Also clear these specific keys just to be sure
localStorage.removeItem('accessToken');
localStorage.removeItem('refreshToken');
localStorage.removeItem('user');

console.log('✅ All authentication data cleared!');
console.log('Now refresh the page and log in again.');
