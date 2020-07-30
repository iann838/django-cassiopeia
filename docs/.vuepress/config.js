const { description } = require('../../package')

module.exports = {
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#title
   */
  title: 'Django Cassiopeia',
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#description
   */
  description: description,

  base: "/django-cassiopeia/",

  /**
   * Extra tags to be injected to the page HTML `<head>`
   *
   * ref：https://v1.vuepress.vuejs.org/config/#head
   */
  head: [
    ['meta', { name: 'theme-color', content: '#3eaf7c' }],
    ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }]
  ],

  /**
   * Theme configuration, here is the default theme configuration for VuePress.
   *
   * ref：https://v1.vuepress.vuejs.org/theme/default-theme-config.html
   */
  themeConfig: {
    repo: '',
    editLinks: false,
    docsDir: '',
    editLinkText: '',
    lastUpdated: false,
    nav: [
      {
        text: 'Documentation',
        link: '/documentation/',
      },
      {
        text: 'Github',
        link: 'https://github.com/paaksing/django-cassiopeia'
      },
      {
        text: 'VuePress',
        link: 'https://v1.vuepress.vuejs.org'
      }
    ],
    sidebar: {
      '/documentation/': [
        {
          title: 'Introduction',
          collapsable: false,
          children: [
            '',
            'examples',
          ]
        },
        {
          title: 'Configuration',
          collapsable: false,
          children: [
            'common',
            'riotapi',
            'pipeline',
            'plugin',
          ]
        },
        {
          title: 'About',
          collapsable: false,
          children: [
            'github',
          ]
        },
        {
          title: 'Migration',
          collapsable: false,
          children: [
            'migrating1to2',
          ]
        },
      ],
    }
  },

  /**
   * Apply plugins，ref：https://v1.vuepress.vuejs.org/zh/plugin/
   */
  plugins: [
    '@vuepress/plugin-back-to-top',
    '@vuepress/plugin-medium-zoom',
  ]
}
