"use client"
import React, { useEffect } from 'react';
import ScrollSection from '@/components/ScrollSections/ScrollSection';
import NavBarFunc from '@/components/Navbar/Navbar';
import MatchCard from '@/components/MatchCard/MatchCard';

export default function Homepage() {
  return (
    <>
      <NavBarFunc />
      <ScrollSection sectionId={'section-one'} bgColor={"blue"}>
        <MatchCard phoenixTeam={"Open"}/>
        <MatchCard phoenixTeam={"O30"}/>
        <MatchCard phoenixTeam={"O40"}/>
      </ScrollSection>
      <ScrollSection sectionId={'section-two'} bgColor={"orange"} />
    </>
  )
}
