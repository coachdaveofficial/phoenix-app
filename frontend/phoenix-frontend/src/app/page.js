"use client"
import React, { useEffect } from 'react';
import ScrollSection from '@/components/ScrollSections/ScrollSection';
import NavBarFunc from '@/components/Navbar/Navbar';
import MatchCard from '@/components/MatchCard/MatchCard';

export default function Homepage() {
  return (
    <>
      <NavBarFunc />
      <ScrollSection sectionId={'section-one'} text={"1"} bgColor={"blue"}>
        <MatchCard phoenixTeam={"Open"}/>
        <MatchCard phoenixTeam={"O30"}/>
        <MatchCard phoenixTeam={"o40"}/>
      </ScrollSection>
      <ScrollSection sectionId={'section-two'} text={"2"} bgColor={"orange"} />
    </>
  )
}
