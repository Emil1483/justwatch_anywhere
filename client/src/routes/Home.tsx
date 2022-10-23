import { useState } from 'react';
import { Link } from 'react-router-dom';

import { SearchResult } from '../models/search-result';

function Home() {
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  let searchQuery = '';

  async function fetchSearchResults(query: string) {
    searchQuery = query;

    const apiUrl = process.env.REACT_APP_API_URL

    const response = await fetch(`${apiUrl}/search?q=${query}`)

    const searchResults = await response.json() as SearchResult[]

    if (query !== searchQuery) return

    setSearchResults(searchResults)
  }

  return <div>
    <input onChange={(e) => fetchSearchResults(e.currentTarget.value)}></input>
    <ul>
      {searchResults.map(s => <li>
        <Link to={`${s.object_type}/${s.id}`}>{s.title}</Link>
      </li>)}
    </ul>
  </div>
}

export default Home;
