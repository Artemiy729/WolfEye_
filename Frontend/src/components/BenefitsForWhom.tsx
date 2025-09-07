import { Container } from '../ui/Container'
import { Card } from '../ui/Card'

interface AudienceItem {
  title: string
  description: string
}

const audience: AudienceItem[] = [
  { title: 'HR и рекрутеры', description: 'Быстрая проверка резюме на накрутки и аномалии.' },
  { title: 'Тимлиды', description: 'Оценка релевантности кандидата задачам команды.' },
  { title: 'Основатели/CEO', description: 'Снижение рисков найма и экономия бюджета.' }
]

export function BenefitsForWhom() {
  return (
    <section className="py-16 text-white">
      <Container>
        <h2 className="text-3xl md:text-4xl font-bold mb-8">Кому может быть полезно</h2>

        <div className="grid gap-6 md:grid-cols-3">
          {audience.map((item) => (
            <Card key={item.title} className="h-full">
              <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
              <p className="text-gray-300">{item.description}</p>
            </Card>
          ))}
        </div>
      </Container>
    </section>
  )
}


