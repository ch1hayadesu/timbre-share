<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">帮助</h1>
      <p class="page-desc">使用指南与常见问题</p>
    </div>

    <Card>
      <h3 class="panel-title">📖 快速入门</h3>
      <div class="help-section">
        <div class="help-step">
          <span class="step-num">1</span>
          <div>
            <div class="step-title">克隆音色</div>
            <div class="step-desc">上传一段语音样本，AI 自动学习音色特征并生成克隆模型。</div>
          </div>
        </div>
        <div class="help-step">
          <span class="step-num">2</span>
          <div>
            <div class="step-title">TTS 合成</div>
            <div class="step-desc">选择音色，输入文本，AI 将用该音色朗读文本内容。</div>
          </div>
        </div>
        <div class="help-step">
          <span class="step-num">3</span>
          <div>
            <div class="step-title">剧本配音</div>
            <div class="step-desc">上传剧本文件，AI 自动识别角色、分析情感，为每个角色匹配不同音色。</div>
          </div>
        </div>
        <div class="help-step">
          <span class="step-num">4</span>
          <div>
            <div class="step-title">音色市场</div>
            <div class="step-desc">探索社区分享的音色，一键下载到你的语音库。</div>
          </div>
        </div>
      </div>
    </Card>

    <Card style="margin-top:var(--space-4);">
      <h3 class="panel-title">❓ 常见问题</h3>
      <div class="faq-list">
        <div v-for="(faq, i) in faqs" :key="i" class="faq-item" @click="toggleFaq(i)">
          <div class="faq-q">
            <span>{{ faq.q }}</span>
            <span class="faq-arrow" :class="{ open: faq.open }">▸</span>
          </div>
          <div v-if="faq.open" class="faq-a">{{ faq.a }}</div>
        </div>
      </div>
    </Card>

    <Card style="margin-top:var(--space-4);">
      <h3 class="panel-title">📞 联系我们</h3>
      <div class="contact-list">
        <div class="contact-item">项目地址：github.com/ch1hayadesu/timbre-share</div>
        <div class="contact-item">技术栈：FastAPI + Vue3 + MySQL + edge-tts</div>
        <div class="contact-item">版本：正式版 1.0</div>
      </div>
    </Card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Card from '@/components/Card.vue'

const faqs = ref([
  { q: '支持哪些音频格式？', a: '支持 WAV、MP3 格式，建议使用 16kHz 采样率、单声道 WAV 文件以获得最佳克隆效果。', open: false },
  { q: '克隆需要多长时间？', a: '即时克隆约 10-30 秒，深度克隆需要 1-5 分钟，具体取决于音频长度和系统负载。', open: false },
  { q: '支持哪些语言？', a: '当前支持中文普通话，后续将支持方言和英文。', open: false },
  { q: '音色可以分享给别人吗？', a: '可以。在「我的音色」中选择音色点击分享，即可发布到音色市场供其他用户下载使用。', open: false },
  { q: '如何下载市场中的音色？', a: '在「音色市场」浏览音色，点击下载按钮即可将音色添加到你的语音库。', open: false },
])

function toggleFaq(i) {
  faqs.value[i].open = !faqs.value[i].open
}
</script>

<style scoped>
.panel-title {
  font-size: var(--font-size-md);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--space-4);
}

.help-section { display: flex; flex-direction: column; gap: var(--space-4); }
.help-step { display: flex; gap: var(--space-4); align-items: flex-start; }
.step-num {
  width: 32px; height: 32px; border-radius: 50%;
  background: var(--color-primary-6); color: white;
  display: flex; align-items: center; justify-content: center;
  font-weight: 600; font-size: 14px; flex-shrink: 0;
}
.step-title { font-weight: 600; font-size: var(--font-size-base); color: var(--color-text-primary); margin-bottom: 4px; }
.step-desc { font-size: var(--font-size-sm); color: var(--color-text-secondary); line-height: 1.6; }

.faq-list { display: flex; flex-direction: column; }
.faq-item {
  padding: var(--space-3) 0; border-bottom: 1px solid var(--color-border-light);
  cursor: pointer;
}
.faq-item:last-child { border-bottom: none; }
.faq-q {
  display: flex; justify-content: space-between; align-items: center;
  font-weight: 500; font-size: var(--font-size-base); color: var(--color-text-body);
}
.faq-arrow { transition: transform var(--duration-fast); font-size: 14px; }
.faq-arrow.open { transform: rotate(90deg); }
.faq-a {
  margin-top: var(--space-3); font-size: var(--font-size-sm);
  color: var(--color-text-secondary); line-height: 1.6;
}

.contact-list { display: flex; flex-direction: column; gap: var(--space-2); }
.contact-item { font-size: var(--font-size-sm); color: var(--color-text-secondary); }
</style>
