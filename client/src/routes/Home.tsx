import { useState } from 'react';
import { Link } from 'react-router-dom';

import { SearchResult } from '../models/search-result';

function Home() {
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);

  async function onChange(e: React.FormEvent<HTMLInputElement>) {
    const apiUrl = process.env.REACT_APP_API_URL

    const query = e.currentTarget.value
    const response = await fetch(`${apiUrl}/search?q=${query}`)
    const searchResults = await response.json() as SearchResult[]
    setSearchResults(searchResults)
  }

  return <div>
    <input onChange={onChange}></input>
    <ul>
      {searchResults.map(s => <li>
        <Link to={`${s.object_type}/${s.id}`}>{s.title}</Link>
      </li>)}
    </ul>
  </div>
}

export default Home;
