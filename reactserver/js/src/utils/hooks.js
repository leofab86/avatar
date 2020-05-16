import {useEffect} from 'react';

export function useClickOutside ({container, handler, listenerConditional = true}, dependencies) {
  useEffect(() => {
    if(listenerConditional) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, dependencies);
  function handleClickOutside (e) {
    if(!container.current.contains(e.target)) {
      handler()
    }
  }
}