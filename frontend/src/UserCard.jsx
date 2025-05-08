import React from 'react';


function UserCard({user}) {
    return (
        <div className="card_container">
            <div className="card_content">
                <img src={user.avatar_url} alt={user.name}/>
                <h3>{user.name}</h3>
                <p><b>Login:</b> {user.login}</p>
                <p><b>Location:</b> {user.location}</p>
                <p><b>Company:</b> {user.company}</p>
                <p><b>Email:</b> {user.email}</p>
                <p><b>Bio:</b> {user.bio}</p>

                <p><b>Followers:</b> {user.followers}</p>
                <p><b>Following:</b> {user.following}</p>
                <p><b>Public repos:</b> {user.public_repos}</p>

                <p><a href={user.html_url} target="_blank">View profile</a></p>
            </div>
        </div>
    );
}

export default UserCard;