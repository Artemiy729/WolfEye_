import { useState } from 'react'
import { Header } from '../../components/Header'
import { HeaderSection } from '../../components/HeaderSection'
import { Modal } from '../../ui/Modal'
import { BetaRequestForm } from '../../components/BetaRequestForm'
import { LoginForm } from '../../components/LoginForm'

export function HomeHero() {
  const [isBetaOpen, setIsBetaOpen] = useState(false)
  const [isLoginOpen, setIsLoginOpen] = useState(false)
  const openBeta = () => setIsBetaOpen(true)
  const closeBeta = () => setIsBetaOpen(false)
  const openLogin = () => setIsLoginOpen(true)
  const closeLogin = () => setIsLoginOpen(false)

  return (
    <div className="min-h-screen text-white">
      <Header onOpenBeta={openBeta} onOpenLogin={openLogin} />
      <HeaderSection onOpenBeta={openBeta} />

      <Modal isOpen={isBetaOpen} onClose={closeBeta} title="Оставить заявку для бета-тестирования">
        <BetaRequestForm onSubmit={closeBeta} />
      </Modal>

      <Modal isOpen={isLoginOpen} onClose={closeLogin} title="Войти">
        <LoginForm onSubmit={closeLogin} />
      </Modal>
    </div>
  )
}


