"use client"
import React from 'react';
import ScrollSectionCards from '@/components/ScrollSections/ScrollSectionCards';
import ScrollSectionAbout from '@/components/ScrollSections/ScrollSectionAbout';
import NavBarFunc from '@/components/Navbar/Navbar';
import MatchCard from '@/components/MatchCard/MatchCard';
import About from '@/components/About/About';
import LoginForm from '@/components/Auth/LoginForm';
import login from '@/helpers/login'

export default function Homepage() {
  return (
    <>
      <NavBarFunc />
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
      <LoginForm login={login}/>
    </>
  )
}
