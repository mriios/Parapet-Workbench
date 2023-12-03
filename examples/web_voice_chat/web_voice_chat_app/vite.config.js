import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: "/Parapet-Workbench/examples/web_voice_chat/web_voice_chat_app/dist",
});
