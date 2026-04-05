import { openDB } from 'idb/with-async-ittr';

const CACHE_NAME = 'api-cache';
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes cache duration

let dbInstance = null;

const getDB = async () => {
  if (!dbInstance) {
    dbInstance = await openDB('staking-dashboard-cache', 1, {
      upgrade(db) {
        db.createObjectStore('cache');
      },
    });
  }
  return dbInstance;
};

const isOnline = () => {
  return navigator.onLine;
};

const fetchWithCache = async (url, options = {}) => {
  try {
    const cachedResponse = await getCachedData(url);
    if (cachedResponse && Date.now() - cachedResponse.timestamp < CACHE_DURATION) {
      return cachedResponse.data;
    }

    if (!isOnline()) {
      // If we're offline, try to return cached data even if it's stale
      const cached = await getCachedData(url);
      if (cached) {
        return cached.data;
      }
      throw new Error('Network error');
    }

    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    // Cache the response
    await cacheData(url, data);
    
    return data;
  } catch (error) {
    throw error; // Re-throw if we can't serve from cache
  }
};

const cacheData = async (key, data) => {
  try {
    const db = await getDB();
    const tx = db.transaction('cache', 'readwrite');
    const store = tx.objectStore('cache');
    await store.put({ data, timestamp: Date.now() }, key);
    await tx.done;
  } catch (error) {
    console.error('Failed to cache data:', error);
  }
};

const getCachedData = async (key) => {
  try {
    const db = await getDB();
    const tx = db.transaction('cache', 'readonly');
    const store = tx.objectStore('cache');
    const cached = await store.get(key);
    await tx.done;
    return cached;
  } catch (error) {
    console.error('Failed to get cached data:', error);
    return null;
  }
};

export { fetchWithCache, isOnline };