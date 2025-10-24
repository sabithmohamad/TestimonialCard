import './App.css'
import TestimonialCard from './components/TestimonialCard'
import ProfileImage from './assets/profile-thumbnail.png'


function App() {

  return (
    <>
      <TestimonialCard
        image = {ProfileImage}
        alt = "profileimage"
        name = "Sara Dole"
      >
         I&apos;ve been searching for high-quality abstract images for my design
        projects, and I&apos;m thrilled to have found this platform. The variety
        and depth of creativity are astounding!
      </TestimonialCard>
    </>
  )
}

export default App
