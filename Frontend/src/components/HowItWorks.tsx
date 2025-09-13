import { Container } from '../ui/Container'
import { Card } from '../ui/CardForLanding'

interface StepItem {
  title: string
  description: string
}

const steps: StepItem[] = [
  { title: '1.  Выберите вакансию', description: 'Выберите открытую вакансию на hh.' },
  { title: '2. Анализ', description: 'Модели выявляют накрутки, аномалии и также проверяет легенду.' },
  { title: '3. Отчет', description: 'Получите оценку риска и рекомендации по вопросам.' }
]

export function HowItWorks() {
  return (
    <section className="py-16 text-white">
      <Container>
        <h2 className="text-3xl md:text-4xl font-bold mb-8">Как это работает</h2>

        <div className="grid gap-6 md:grid-cols-3">
          {steps.map((step) => (
            <Card key={step.title} className="h-full">
              <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
              <p className="text-gray-300">{step.description}</p>
            </Card>
          ))}
        </div>
      </Container>
    </section>
  )
}


