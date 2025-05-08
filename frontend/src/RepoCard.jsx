import React from 'react';

function RepoCard({repo}) {
    return (
        <div className="card_container">
            <div className="card_content">
                <h3>{repo.name}</h3>
                <p><b>Description:</b> {repo.description}</p>
                <p><b>Author:</b> {repo.owner?.login}</p>
                <p><b>Author email:</b> {repo.owner?.email}</p>
                <p><b>Stars:</b> {repo.stargazers_count}</p>
                <p><b>Forks:</b> {repo.forks_count}</p>
                <p><b>Subscribers:</b> {repo.subscribers_count}</p>
                <p><b>license:</b> {repo.license?.name}</p>

                <p><a href={repo.html_url} target="_blank">View repo</a></p>
            </div>
        </div>
    );
}

export default RepoCard;