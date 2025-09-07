import { Button } from '../ui/Button'
import { Container } from '../ui/Container'

interface HeaderProps {
  onOpenBeta?: () => void
  onOpenLogin?: () => void
}

export function Header({ onOpenBeta, onOpenLogin }: HeaderProps) {
  return (
    <header className="w-full border-b border-gray-800/60">
      <Container>
        <div className="flex items-center justify-between py-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full border-2 border-cyan-400 flex items-center justify-center">
              <svg className="w-5 h-5 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z" />
                <circle cx="12" cy="12" r="3" fill="currentColor" />
              </svg>
            </div>
            <span className="text-white font-bold text-2xl">ГЛАЗ ВОЛКА</span>
          </div>

          {/* Новый круг по центру */}
          <div className="w-24 h-24 rounded-full border-2 border-cyan-400 flex items-center justify-center mx-auto">
            <svg className="w-12 h-12 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z" />
              <circle cx="12" cy="12" r="3" fill="currentColor" />
            </svg>
          </div>

          <div className="flex items-center space-x-3">
            <Button onClick={onOpenLogin} variant="ghost" size="lg">Войти</Button>
            <Button onClick={onOpenBeta} variant="primary" size="lg" className="custom-button-bg">Оставить Заявку</Button>
          </div>
        </div>
      </Container>
    </header>
  )
}