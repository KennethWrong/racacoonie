import React from "react";
import { Link } from "react-router-dom";
import { useTheme } from '@mui/material/styles';
import Dropdownbar from "../components/Dropdownbar"



const Homepage = () => {

      
  return (
    <div>
      <p>Hi</p>
      <Dropdownbar></Dropdownbar>
      <Link to="/login">
        <button
          type="button"
          className="flex flex-col  text-gray-900 bg-blue-200 border border-blue-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-full text-sm px-5 py-2.5 mr-2 mb-2 mx-auto dark:bg-blue-900 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"
        >
          Login
        </button>
      </Link>
    </div>
  );
};

export default Homepage;
