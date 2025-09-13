import type { ReactNode } from 'react'
import { useEffect } from 'react'
import { createPortal } from 'react-dom'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  children: ReactNode
  widthClassName?: string
}

export function Modal({ isOpen, onClose, title, children, widthClassName = 'max-w-lg' }: ModalProps) {
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose()
    }
    if (isOpen) document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [isOpen, onClose])

  if (!isOpen) return null

  return createPortal(
    <div className="fixed inset-0 z-50">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div className="absolute inset-0 flex items-center justify-center p-4">
        <div className={`w-full ${widthClassName} bg-gray-900 text-white rounded-xl border border-gray-800 shadow-2xl`}>
          <div className="flex items-center justify-between px-5 py-4 border-b border-gray-800">
            <h3 className="text-lg font-semibold">{title}</h3>
            <button onClick={onClose} aria-label="Close" className="text-gray-400 hover:text-white">✕</button>
          </div>
          <div className="px-5 py-4">{children}</div>
        </div>
      </div>
    </div>,
    document.body
  )
}



