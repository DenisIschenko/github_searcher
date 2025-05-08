import React, {useCallback, useEffect, useState} from 'react';
import axios from 'axios';
import debounce from 'lodash.debounce';
import SearchForm from './SearchForm';
import UserCard from './UserCard';
import RepoCard from './RepoCard';


function App() {
    const [query, setQuery] = useState('');
    const [entity, setEntity] = useState('users');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");


    const fetchResults = useCallback(
        debounce(async (query, entity) => {
            if (query.length < 3) {
                setResults([]);
                setError("");
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                setError("");
                const res = await axios.post(`/api/search`, {
                    query: query, type: entity.toLowerCase()
                });
                setResults(res.data);
                console.log(res.data[0]);
            } catch (err) {
                console.error("Error fetching data:", err);
                setError("Failed to fetch data.");
            } finally {
                setLoading(false);
            }
        }, 500),
        []
    );

    useEffect(() => {
        if (query.length >= 3) {
            fetchResults(query, entity);
        } else {
            setResults([]);
        }
    }, [query, entity, fetchResults]);

    const handleQueryChange = (value) => setQuery(value);
    const handleEntityChange = (value) => setEntity(value);

    return (
        <div className="app_container">
            <div className={"container"}>
                <div className={"title_form"}>

                    <img
                        src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
                        alt="GitHub Logo"
                        style={{width: 48, height: 48}}
                    />
                    <div className={"title"}>
                        <h3>GitHub Searcher</h3>
                        <p>Search users or repositories below</p>
                    </div>
                </div>
                <SearchForm
                    query={query}
                    entity={entity}
                    loaning={loading}
                    onQueryChange={handleQueryChange}
                    onEntityChange={handleEntityChange}
                />

                {loading && (
                    <div className="loader_container">
                        <div className="loader"></div>
                    </div>
                )}

                {error && (
                    <div className="error_container">
                        {/*{error.map((error, i) => <p key={i}>{error.value}</p>}*/}
                        <p>{error}</p>
                    </div>
                )}

                {!loading && results.length > 0 && (
                    <div className="response_container">
                        {results.map((item, index) =>
                            entity === 'users' ? (
                                <div className="item_container" key={index}>
                                    <UserCard user={item}/>
                                </div>
                            ) : (
                                <div className="item_container" key={index}>
                                    <RepoCard repo={item}/>
                                </div>
                            )
                        )}
                    </div>
                )}

                {!loading && results.length === 0 && query.length < 3 && (
                    <h6 align="center">
                        Please enter at least 3 characters to search.
                    </h6>
                )}
            </div>
        </div>
    );
}

export default App;