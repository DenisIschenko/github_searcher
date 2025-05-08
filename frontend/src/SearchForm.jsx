import React from "react";
import Select from 'react-select';

function SearchForm({query, entity, loaning, onQueryChange, onEntityChange}) {
    const options = [
        {value: 'users', label: 'User'},
        {value: 'repositories', label: 'Repository'}
    ]
    return (
        <div className="search_form">
            <input name="search_input"
                   placeholder="Search"
                   value={query}
                   onChange={(e) => onQueryChange(e.target.value)}
                   disabled={loaning}
            />
            <Select
                onChange={(e) => onEntityChange(e.value)}
                // value={entity}
                value={options.filter(function(option) {
                    return option.value === entity;
                })}
                // defaultValue={entity}
                className="react_select_container"
                options={options}
                isSearchable={false}
                isDisabled={loaning}
            />
        </div>
    );
}

export default SearchForm;