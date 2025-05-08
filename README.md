## High-Level Solution Overview

This project consists of a backend implemented with Django and a frontend built using React.

### Backend

The backend provides API endpoints for searching GitHub and clearing the cache. A caching mechanism was implemented to store search queries for 2 hours to reduce the number of external requests to the GitHub API.

During development, it became clear that the GitHub search API does not return complete information about repositories and users. Therefore, additional logic was implemented to fetch full user details separately. Since this process is relatively resource-intensive, those requests are also cached for 2 hours.

Automated tests were written to ensure the correctness of the implemented logic.

### Frontend

The frontend uses the `react-select` library to style the select component in the form. The default HTML select element does not allow for sufficient customization, and building a fully custom select component from scratch would have been too time-consuming.

While the visual design of the repository and user cards is minimal and not ideal, it reflects a conscious trade-off due to limited time and lack of design expertise. All fields received from the backend are passed to the frontend, but not all of them are displayed. I think, the main focus was on retrieving the complete data — visual presentation was considered secondary.

### Notes

- The system is designed with extensibility and performance in mind, using caching to mitigate GitHub's rate limits.
- Code and structure are organized for clarity and testability.