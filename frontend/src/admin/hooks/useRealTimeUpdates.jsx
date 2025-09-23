import { useState, useEffect, useRef, useCallback } from 'react';

const useRealTimeUpdates = (refreshInterval = 30000) => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const intervalRef = useRef(null);

  const connect = useCallback(() => {
    // Simulate WebSocket connection
    setIsConnected(true);
    console.log('Real-time updates connected');

    // Set up periodic updates
    intervalRef.current = setInterval(() => {
      setLastUpdate(new Date());
      // In a real app, this would trigger data refresh
    }, refreshInterval);
  }, [refreshInterval]);

  const disconnect = useCallback(() => {
    setIsConnected(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    console.log('Real-time updates disconnected');
  }, []);

  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    isConnected,
    lastUpdate,
    connect,
    disconnect
  };
};

export default useRealTimeUpdates;
