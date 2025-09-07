import { Button } from '../ui/Button'
import { Container } from '../ui/Container'
import { TextBlock } from '../ui/TextBlock'

interface HeaderSectionProps {
  onOpenBeta?: () => void
}

export function HeaderSection({ onOpenBeta }: HeaderSectionProps) {
  return (
    <section className="relative overflow-hidden py-16 md:py-24">
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-gray-900 via-blue-900/20 to-cyan-900/20" />

      <Container>
        <div className="max-w-5xl mx-0">
          <TextBlock
              title="Найдите лучших IT специалистов без накруток"
              subtitle='PDF-ки или ссылки на hh → рейтинг, red‑флаги и вопросы за 1 минуту.'
              content="Попробуйте демо: выявляем накрутки, подсвечиваем риски, даём вопросы для верификации."
          />

          <div className="mt-8">
            <Button onClick={onOpenBeta} variant="primary" size="lg" className="custom-button-bg text-lg px-8 py-4">
              Получить Демо
            </Button>
          </div>
        </div>
      </Container>
    </section>
  )
}


