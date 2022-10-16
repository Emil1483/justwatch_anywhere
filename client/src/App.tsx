import React, { useState } from 'react';
import './App.css';
import { SearchResults as SearchResult } from './models/search-results';

function App() {
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);

  async function onChange(e: React.FormEvent<HTMLInputElement>) {
    const query = e.currentTarget.value
    const response = await fetch(`https://justwatch-anywhere.vercel.app/search?q=${query}`)
    const searchResults = await response.json() as SearchResult[]
    setSearchResults(searchResults)
  }

  return <div>
    <input onChange={onChange}></input>
    <ul>
      {searchResults.map(s => <li>{s.title}</li>)}
    </ul>
  </div>
}

export default App;
