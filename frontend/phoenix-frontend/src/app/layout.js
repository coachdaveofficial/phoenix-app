import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Phoenix FC',

}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${inter.className} 
      bg-slate-800
      text-slate-100

      mx-auto
      `}>
        
        
        {children}</body>
    </html>
  )
}
