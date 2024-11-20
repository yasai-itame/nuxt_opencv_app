<script setup lang="ts">

type Result = {
  encode_image: string
}

const isEncodeImage = (result: Result): result is Result => {
  return (result as Result).encode_image !== undefined
}

const displayCheck = ref<boolean>(false)
const previewImage = ref<string | ArrayBuffer | null | undefined>("")
const imageData = ref<File>()

const fileUp = (event: Event):void => {
  if (!(event.target instanceof HTMLInputElement)) {
    displayCheck.value = false
    return
  }
  const data = event.target as HTMLInputElement
  if (!data.files) return
  const file = data.files[0]
  const reader = new FileReader()
  reader.onload = (event: ProgressEvent<FileReader>) => {
    previewImage.value = event.target?.result
    imageData.value = file
    displayCheck.value = true
  }
  reader.readAsDataURL(file)
  event.target.value = ""
}

const submitData = async (type: string) => {
  const formData = new FormData()
  if (!imageData.value) return
  formData.append('file', imageData.value)
  formData.append('type', type)
  let result:Result = await $fetch('/opencv', {
    method: 'POST',
    body: formData
  })
  if (isEncodeImage(result)) {
    previewImage.value = 'data:image/png;base64,' + result.encode_image
  }
}
</script>

<template>
  <div class="h-screen leading-normal tracking-normal text-indigo-400 p-8 bg-cover bg-fixed bg-gradient-to-t from-teal-300 to-indigo-600">
    <div class="h-full flex justify-center items-center">
      <!--Main-->
      <div class="container mx-auto flex flex-wrap flex-col md:flex-row items-center justify-between">
        <!--Left Col-->
        <div class="flex flex-col w-full xl:w-2/5 justify-center lg:items-start overflow-y-hidden">
          <h1 class="my-4 text-3xl md:text-5xl text-white opacity-75 font-bold leading-tight text-center md:text-left">
            Image Change
          </h1>

          <div class="bg-gray-900 opacity-75 w-full shadow-lg rounded-lg px-8 pt-6 pb-8 mb-4">
            <div class="mb-4">
              <label class="text-base text-gray-500 font-semibold mb-2 block">Upload file</label>
              <input @change="fileUp" type="file" accept="image/*"
                class="w-full text-gray-400 font-semibold text-sm bg-white border file:cursor-pointer cursor-pointer file:border-0 file:py-3 file:px-4 file:mr-4 file:bg-gray-100 file:hover:bg-gray-200 file:text-gray-500 rounded" />
              <p class="text-xs text-gray-400 mt-2">PNG, JPG SVG, WEBP, and GIF are Allowed.</p>
            </div>

            <div class="flex items-center pt-4">
              <button
                @click="submitData('gray')"
                :disabled="!imageData"
                class="bg-neutral-400 from-purple-800 to-green-500 hover:from-pink-500 hover:to-green-500 text-white font-bold py-2 px-4 rounded focus:ring transform transition hover:scale-105 duration-300 ease-in-out"
                type="button"
              >
                グレースケール
              </button>
              <button
                @click="submitData('mosaic')"
                :disabled="!imageData"
                class="bg-green-800 from-purple-800 to-green-500 hover:from-pink-500 hover:to-green-500 text-white font-bold py-2 px-4 rounded focus:ring transform transition hover:scale-105 duration-300 ease-in-out ml-2"
                type="button"
              >
                モザイク
              </button>
              <button
                @click="submitData('edge')"
                :disabled="!imageData"
                class="bg-red-800 from-purple-800 to-green-500 hover:from-pink-500 hover:to-green-500 text-white font-bold py-2 px-4 rounded focus:ring transform transition hover:scale-105 duration-300 ease-in-out ml-2"
                type="button"
              >
                エッジ
              </button>
              <button
                @click="submitData('rotation')"
                :disabled="!imageData"
                class="bg-yellow-800 from-purple-800 to-green-500 hover:from-pink-500 hover:to-green-500 text-white font-bold py-2 px-4 rounded focus:ring transform transition hover:scale-105 duration-300 ease-in-out ml-2"
                type="button"
              >
                反転
              </button>
            </div>
          </div>
        </div>

        <!--Right Col-->
        <div class="w-full xl:w-3/6 overflow-hidden">
          <div v-if="displayCheck" class="overflow-hidden h-96 relative">
            <img :src="typeof previewImage === 'string' ? previewImage : ''" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 h-96 rounded-lg" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
