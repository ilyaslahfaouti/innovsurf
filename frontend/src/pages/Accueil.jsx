import React from 'react';
import './Accueil.css';  
import videoSrc from '../assets/video/surf.mp4'; 

import blogImage1 from '../assets/banana.png';
import blogImage2 from '../assets/bouznika.jpg';
import blogImage3 from '../assets/taghazout.jpg';

const Accueil = () => {
  return (
    <div className='AccueilPage'>
      <div className="hero-section">
        <div className="hero-content">
          <h1> Innov Surf</h1>
          <p>Your go-to platform for everything surf-related in Morocco. Designed for both beginners and seasoned surfers, as well as surf clubs.</p>
          <a href="#details" className="cta-button">More Details</a>
        </div>
        <div className="scroll-indicator">
          <i  className="fas fa-angle-down"></i>
        </div>
      </div>

      <div className="meet-flowspark-section">
        <div className="meet-flowspark-content">
          <h2>Let's ride it</h2>
          <p id='details'> Riding waves feels like dancing with nature. As you rise on your board, there’s a rush of adrenaline mixed with pure joy. </p>
        </div>
        <div className="meet-flowspark-details">
          <div className="video-placeholder">
            <video autoPlay loop muted>
              <source src={videoSrc} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
          <div className="mission-statement">
            <h3>Our Mission</h3>
            <p>
            At Innov Surf, our mission is to create a seamless experience for surfers and surf clubs across Morocco. We believe that surfing is more than just a sport—it’s a lifestyle, a community, and a connection with nature. 
            </p>
            <p>
            Whether you're organizing lessons, managing equipment rentals, or promoting surf events, Innov Surf is here to help your club thrive.
            </p>
            <a href="/contact" className="cta-button">Contact Us</a>
          </div>
        </div>
      </div>

      <div className="latest-from-blog-section">
        <h2>Popular Spots</h2>
        <p>Here are some of the most popular surfing spots in Morocco !</p>
        <div className="blog-posts">
          <div className="blog-post">
            <img src={blogImage1} alt="Blog Post 1" />
            <div className="post-category">Beginner</div>
            <h3>Banana Beach</h3>
            <p>Banana Point is a surf spot nestled between the mouth of the Tamraght river and a rocky point that offers protection from the northern winds.</p>
          </div>
          <div className="blog-post">
            <img src={blogImage2} alt="Blog Post 2" />
            <div className="post-category">Intermediate</div>
            <h3>La crique in Bouznika</h3>
            <p>Nestled along the captivating coast of Morocco, La crique surf spot emerges as a perfect A-Frame, enchanting wave seekers with its consistent waves and vibrant surf culture.</p>
          </div>
          <div className="blog-post">
            <img src={blogImage3} alt="Blog Post 3" />
            <div className="post-category">Advanced</div>
            <h3>Anchor Point </h3>
            <p>Located north of the village of Taghazout. It’s a world-class right-hand break that works best with a long-period northwest swell. Discovered by Australians in the 1960s</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Accueil;
