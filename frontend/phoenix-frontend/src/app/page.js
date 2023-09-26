"use client"
import React, { useState, useEffect } from 'react';
import ScrollSectionCards from '@/components/scrollSections/ScrollSectionCards';
import ScrollSectionAbout from '@/components/scrollSections/ScrollSectionAbout';
import NavBarFunc from '@/components/navbar/Navbar';
import MatchCard from '@/components/matchCard/MatchCard';
import About from '@/components/about/About';
import LoginForm from '@/components/auth/LoginForm';
import login from '@/helpers/login'
import ScriptForm from '@/components/forms/ScriptForm';
import Modal from '@/components/common/Modal';


export default function Homepage() {
  const [showModal, setShowModal] = useState(false);
  const handleModalShow = () => {
    setShowModal(!showModal);
  }
  useEffect(() => {

    // Add an event listener for the ESC key press
    document.addEventListener('keydown', (e) => {
      if (showModal && e.key === 'Escape') {
        handleModalShow();
      }
    });

    // Remove the event listener when the component unmounts
    return () => {
      document.removeEventListener('keydown', handleModalShow);
    };
  }, [showModal]);

  return (
    <>
      <NavBarFunc handleModalShow={handleModalShow} />
      {showModal && <Modal title={"Upload worksheet data"} handleModalShow={handleModalShow}>
        <ScriptForm />
      </Modal>
      }

      <ScrollSectionCards sectionId={'section-one'} bgColor={"blue"}>
        <MatchCard phoenixTeam={"Open"} />
        <MatchCard phoenixTeam={"O30"} />
        <MatchCard phoenixTeam={"O40"} />
      </ScrollSectionCards>
      <ScrollSectionAbout sectionId={'section-two'} bgColor={"orange"} >
        <About
          youtubeLink={"https://www.youtube.com/@Phoenix_FC/featured"}
          instagramLink={"https://www.instagram.com/phoenix_fc_pdx/"}
          facebookLink={"https://www.facebook.com/Phoenixfc.pdx"}
          leagueLink={"http://gpsdsoccer.com/"}
          OASALink={"https://www.oregonadultsoccer.com/"}
          indoorLink={"https://pdxindoorsoccer.com/"}
        />
      </ScrollSectionAbout>

    </>
  )
}
