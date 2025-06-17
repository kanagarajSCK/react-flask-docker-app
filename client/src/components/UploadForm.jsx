import React, { useState } from 'react'
import axios from 'axios'
import './UploadForm.css'

const resizeImage = (file, maxWidth, maxHeight) => {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)

    reader.onload = (event) => {
      const img = new Image()
      img.src = event.target.result

      img.onload = () => {
        const canvas = document.createElement('canvas')
        const scale = Math.min(maxWidth / img.width, maxHeight / img.height)
        const width = img.width * scale
        const height = img.height * scale
        canvas.width = width
        canvas.height = height

        const ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0, width, height)

        canvas.toBlob((blob) => {
          const resizedFile = new File([blob], file.name, { type: file.type })
          resolve(resizedFile)
        }, file.type)
      }
    }
  })
}

const UploadForm = () => {
  const [previewUrl, setPreviewUrl] = useState(null)
  const [resultImage, setResultImage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [dragActive, setDragActive] = useState(false)

  const handleDetect = async (file) => {
    if (!file) return
    setLoading(true)
    const resizedFile = await resizeImage(file, 500, 500)
    setPreviewUrl(URL.createObjectURL(resizedFile))
    const formData = new FormData()
    formData.append('image', resizedFile)

    try {
      const res = await axios.post('http://localhost:5000/detect', formData)
      setResultImage(`data:image/jpeg;base64,${res.data.image}`)
    } catch (error) {
      alert('❌ Detection failed. Try another image.')
    } finally {
      setLoading(false)
    }
  }

  const handleFileChange = async (e) => {
    const file = e.target.files[0]
    await handleDetect(file)
  }

  const handleDrop = async (e) => {
    e.preventDefault()
    setDragActive(false)
    const file = e.dataTransfer.files[0]
    await handleDetect(file)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setDragActive(true)
  }

  const handleDragLeave = () => {
    setDragActive(false)
  }

  return (
    <div className="bg-white text-black rounded-2xl p-8 shadow-2xl w-full max-w-2xl mx-auto animate-fade-in">
      <h2 className="text-2xl font-bold mb-6 text-center">Age & Gender Detection</h2>

      {/* Drop Image Box */}
      <div
  onDrop={handleDrop}
  onDragOver={handleDragOver}
  onDragLeave={handleDragLeave}
  className={`drop-zone w-full h-40 rounded-xl flex items-center justify-center text-gray-700 font-semibold transition-all ${
    dragActive ? 'bg-blue-100 border-blue-500 border-4' : 'bg-gray-100 border-gray-300 border-2'
  }`}
>
  <p>👉 Drag & Drop Image Here</p>
</div>


      {/* OR separator */}
      <div className="text-gray-500 text-center my-4 font-semibold">OR</div>

      {/* Choose File Option */}
      <div className="flex flex-col items-center gap-4">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="border border-gray-300 rounded px-4 py-2 text-gray-700 shadow-sm file:cursor-pointer"
        />
      </div>

      {/* Preview */}
      {previewUrl && !resultImage && (
        <div className="mt-6 text-center">
          <h3 className="text-sm text-gray-500 mb-2">Preview (Resized)</h3>
          <img
            src={previewUrl}
            alt="Preview"
            className="mx-auto rounded border w-full max-w-sm max-h-[300px] object-contain"
          />
        </div>
      )}

      {/* Result */}
      {resultImage && (
        <div className="mt-6 text-center">
          <h3 className="text-sm text-gray-700 mb-2">Detected Result</h3>
          <img
            src={resultImage}
            alt="Detected"
            className="mx-auto rounded-lg border-4 border-green-500 shadow-lg w-full max-w-sm max-h-[400px] object-contain"
          />
        </div>
      )}

      {/* Loading */}
      {loading && (
  <div className="flex flex-col items-center mt-6">
    <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
    <p className="mt-2 text-blue-600 font-medium">Detecting...</p>
  </div>
)}

    </div>
  )
}

export default UploadForm
