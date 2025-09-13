import { useState } from 'react'
import { Container } from '../ui/Container'
import { Card } from '../ui/CardForLanding'
import { Modal } from './ModalComponent'

export function Confidentiality() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <footer className="py-10 text-white border-t border-gray-800/60 bg-[#0e1a30]">
      <Container>
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
          <div className="text-2xl font-extrabold tracking-wide">ГЛАЗ ВОЛКА</div>

          <nav className="flex flex-col sm:flex-row gap-4 text-gray-300">
            <button type="button" onClick={() => setIsOpen(true)} disabled className="text-left text-gray-500 cursor-not-allowed">
              Политика конфиденциальности
            </button>
          </nav>

          <div className="text-sm text-gray-400">© {new Date().getFullYear()} Все права защищены</div>
        </div>
      </Container>

      <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Политика конфиденциальности">
        <div className="space-y-4 text-gray-300">
          <p>
            Мы обрабатываем документы локально и безопасно. Данные не передаются третьим лицам и
            не используются для обучения моделей без вашего согласия.
          </p>
          <p>
            По запросу мы удалим все загруженные материалы и связанные метаданные. Для связи
            используйте форму обратной связи или напишите на support@wolfeye.ai.
          </p>
          <Card className="bg-gray-800/60">
            <ul className="list-disc pl-5 text-sm">
              <li>Храним только необходимые технические метаданные</li>
              <li>Шифруем данные при передаче и хранении</li>
              <li>Доступ ограничен авторизованным персоналом</li>
            </ul>
          </Card>
        </div>
      </Modal>
    </footer>
  )
}


