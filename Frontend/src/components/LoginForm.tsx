import type { FormEvent } from 'react'
import { useState } from 'react'
import { Button } from '../ui/Button'

interface LoginFormProps {
  onSubmit?: (data: { email: string; password: string;}) => void
}

export function LoginForm({ onSubmit }: LoginFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!email || !password) {
      setError('Почта, Пароль')
      return
    }
    setError(null)
    onSubmit?.({ email, password })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <div className="text-red-400 text-sm">{error}</div>}

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
        <span className="block mb-1 text-sm text-gray-300">Пароль*</span>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white outline-none focus:ring-2 focus:ring-cyan-500"
          placeholder="••••••••"
        />
      </label>

      <div className="pt-2">
        <Button type="submit" variant="primary" className="custom-button-bg w-full">Войти</Button>
      </div>
    </form>
  )
}


