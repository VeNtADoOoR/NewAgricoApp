// src/axios.js
import axios from 'axios';

// Ensure credentials are included
axios.defaults.withCredentials = true;

// Add CSRF token to headers
axios.defaults.headers.common['X-CSRF-TOKEN'] = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

export default axios;
