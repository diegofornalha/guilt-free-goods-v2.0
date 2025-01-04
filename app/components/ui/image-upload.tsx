'use client';

import { useState } from 'react';
import { Upload, Image as ImageIcon, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ImageUploadProps {
  onUpload?: (file: File) => void;
  className?: string;
}

export function ImageUpload({ onUpload, className }: ImageUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      await handleFileUpload(file);
    }
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      await handleFileUpload(file);
    }
  };

  const handleFileUpload = async (file: File) => {
    setIsUploading(true);
    try {
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);

      // Call onUpload callback if provided
      if (onUpload) {
        await onUpload(file);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div
      className={cn(
        'relative flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg transition-colors',
        isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300',
        className
      )}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <input
        type="file"
        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        onChange={handleFileSelect}
        accept="image/*"
      />
      
      {isUploading ? (
        <div className="flex flex-col items-center">
          <Loader2 className="w-10 h-10 text-blue-500 animate-spin" />
          <p className="mt-2 text-sm text-gray-500">Uploading...</p>
        </div>
      ) : preview ? (
        <div className="relative w-full h-full">
          <img
            src={preview}
            alt="Preview"
            className="object-contain w-full h-full"
          />
          <button
            onClick={() => setPreview(null)}
            className="absolute top-2 right-2 p-1 bg-white rounded-full shadow-md hover:bg-gray-100"
          >
            <ImageIcon className="w-4 h-4" />
          </button>
        </div>
      ) : (
        <div className="flex flex-col items-center">
          <Upload className="w-10 h-10 text-gray-400" />
          <p className="mt-2 text-sm text-gray-500">
            Drag and drop an image, or click to select
          </p>
        </div>
      )}
    </div>
  );
}
