import { type H3Event } from 'h3'
export default defineEventHandler(async (event: H3Event) => {
  const data = await readMultipartFormData(event)
  if (!data || data.length == 0) return
  const fileData = data.find(item => item.name === 'file')
  const typeData = data.find(item => item.name === 'type')?.data.toString()
  if (!fileData || !typeData) {
    return {
      statusCode: 400,
      body: { error: 'File not found' }
    };
  }

  const fileBlob = new Blob([fileData.data])
  const formData = new FormData();
  formData.append('file', fileBlob, fileData.filename);
  formData.append('type', typeData)
  const result = await $fetch('http://127.0.0.1:8000/result-opencv', {
    method: 'POST',
    body: formData
  })

  return result
})