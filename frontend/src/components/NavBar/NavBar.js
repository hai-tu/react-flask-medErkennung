import React from 'react';
import { Link } from 'react-router-dom';

import './NavBar.css';

const NavBar = () => {
  return (
    <div>
      <ul>
        <li><Link to="/Home">Detection</Link></li>
        <li><Link to="/About">GroundTruth</Link></li>
     	</ul>
    </div>
  );
};

export default NavBar;