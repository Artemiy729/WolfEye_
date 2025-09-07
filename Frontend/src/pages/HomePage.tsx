import { HomeHero } from '../modules/HomeHero'
import { BenefitsForWhom } from '../components/BenefitsForWhom'
import { HowItWorks } from '../components/HowItWorks'
import { Confidentiality } from '../components/Confidentiality'

export function HomePage() {
  return (
    <>
      <HomeHero />
      <BenefitsForWhom />
      <HowItWorks />
      <Confidentiality />
    </>
  )
}

export default HomePage

