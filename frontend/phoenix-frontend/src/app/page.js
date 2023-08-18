"use client"
import { useEffect } from 'react';
import ScrollSection from '@/components/ScrollSections/ScrollSection';
import NavBarFunc from '@/components/Navbar/Navbar';

export default function Homepage() {
  return (
    <>
      <NavBarFunc />
      <ScrollSection sectionId={'section-one'} text={"1"} bgColor={"blue"}/>
      <ScrollSection sectionId={'section-two'} text={"2"} bgColor={"orange"}/>
    </>
  )
}
