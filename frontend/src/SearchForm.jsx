import React from "react";
import Select from 'react-select';

function SearchForm({query, entity, loaning, onQueryChange, onEntityChange}) {
    const options = [
        {value: 'users', label: 'User'},
        {value: 'repositories', label: 'Repository'}
    ]
    const customStyles = {
        control: (styles) => ({
            ...styles,
            borderRadius: "0",
            borderColor: "#b5b4b4",
        }),
        singleValue: (provided) => ({
            ...provided,
            color: "#b5b4b4",
        }),
    }
    return (
        <div className="search_form">
            <input name="search_input"
                   placeholder="Start tuping to search..."
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
                components={{
                    IndicatorSeparator: () => null
                }}
                styles={customStyles}
            />
        </div>
    );
}

export default SearchForm;