

import { Button } from '../ui/Button'
import { Container } from '../ui/Container'
import { Logo } from '../ui/Logo'

interface HeaderProps {
  onOpenBeta?: () => void
  onOpenLogin?: () => void
}

export function Header({ onOpenBeta, onOpenLogin }: HeaderProps) {
  return (
    <header className="w-full border-b border-gray-800/60">
      <Container>
        <div className="flex items-center justify-between py-4">
          <Logo size="md" />

          <Logo size="xl" showText={false} className="mx-auto" />

          <div className="flex items-center space-x-3">
            <Button onClick={onOpenLogin} variant="ghost" size="lg">Войти</Button>
            <Button onClick={onOpenBeta} variant="primary" size="lg" className="custom-button-bg">Оставить Заявку</Button>
          </div>
        </div>
      </Container>
    </header>
  )
}