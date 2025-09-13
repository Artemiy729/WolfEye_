import type { FormEvent } from 'react'
import { useState } from 'react'
import { Button } from '../ui/Button'

interface BetaRequestFormProps {
  onSubmit?: (data: { email: string; telegram?: string; name: string; company: string }) => void
}

export function BetaRequestForm({ onSubmit }: BetaRequestFormProps) {
  const [email, setEmail] = useState('')
  const [telegram, setTelegram] = useState('')
  const [name, setName] = useState('')
  const [company, setCompany] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [isSubmitted, setIsSubmitted] = useState(false)

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!email || !name || !company) {
      setError('Почта, Имя и Компания обязательны')
      return
    }
    setError(null)
    setIsSubmitted(true)
    onSubmit?.({ email, telegram, name, company })
  }

  if (isSubmitted) {
    return (
      <div className="text-center space-y-2">
        <div className="text-xl font-semibold">Заявка отправлена</div>
        <div className="text-gray-300">Мы свяжемся с вами в ближайшее время.</div>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <div className="text-red-400 text-sm">{error}</div>}

      <div className="grid gap-4">
        <label className="block">
          <span className="block mb-1 text-sm text-gray-300">Почта*</span>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white outline-none focus:ring-2 focus:ring-cyan-500"
            placeholder="name@company.com"
          />
        </label>

        <label className="block">
          <span className="block mb-1 text-sm text-gray-300">Тг (username)</span>
          <input
            type="text"
            value={telegram}
            onChange={(e) => setTelegram(e.target.value)}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white outline-none focus:ring-2 focus:ring-cyan-500"
            placeholder="@username"
          />
        </label>

        <label className="block">
          <span className="block mb-1 text-sm text-gray-300">Имя*</span>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white outline-none focus:ring-2 focus:ring-cyan-500"
            placeholder="Иван Иванов"
          />
        </label>

        <label className="block">
          <span className="block mb-1 text-sm text-gray-300">Компания*</span>
          <input
            type="text"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white outline-none focus:ring-2 focus:ring-cyan-500"
            placeholder="ООО Рога и Копыта"
          />
        </label>
      </div>

      <div className="pt-2">
        <Button type="submit" variant="primary" className="custom-button-bg w-full">Оставить заявку</Button>
      </div>
    </form>
  )
}


