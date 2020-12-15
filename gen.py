
template = """
name: [place_holder]

on:
  workflow_dispatch:
  schedule:
    - cron: '[crontab_place_holder]'
  watch:
    types: started
  repository_dispatch:
    types: [place_holder]
jobs:
  build:

    runs-on: ubuntu-latest
    if: github.event.repository.owner.id == github.event.sender.id
    steps:
      - name: Checkout
        uses: actions/checkout@v2
        with:
          repository: btjun/books
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v1
        with:
          node-version: ${{ matrix.node-version }}
      - name: Cache node_modules
        uses: actions/cache@v2 
        env:
          cache-name: cache-node-modules
        with:
          path: node_modules
          key: ${{ runner.os }}-${{ env.cache-name }}-${{ hashFiles('package-lock.json') }} 
      - name: npm install
        run: |
          npm install
      - name: 'running [place_holder]'
        run: |
          node [place_holder]
        env:
          JD_COOKIE: ${{ secrets.JD_COOKIE }}
          JD_DEBUG: ${{ secrets.JD_DEBUG }}
          PUSH_KEY: ${{ secrets.PUSH_KEY }}
          BARK_PUSH: ${{ secrets.BARK_PUSH }}
          BARK_SOUND: ${{ secrets.BARK_SOUND }}
          TG_BOT_TOKEN: ${{ secrets.TG_BOT_TOKEN }}
          TG_USER_ID: ${{ secrets.TG_USER_ID }}
          DD_BOT_TOKEN: ${{ secrets.DD_BOT_TOKEN }}
          DD_BOT_SECRET: ${{ secrets.DD_BOT_SECRET }}
          IGOT_PUSH_KEY: ${{ secrets.IGOT_PUSH_KEY }}

"""

import re

cron_re = "[-|0-9| |,|*|\\/]* \\*"
script_re = "j[_|a-zA-Z]*\\.js"

file = open("./docker/crontab_list.sh", "r", encoding='utf-8')


try:
    text_lines = file.readlines()
    # print(type(text_lines), text_lines)
    for line in text_lines:
        cron = re.search(cron_re, line)
        script = re.search(script_re, line)
        if script:
            print(cron.group(0))
            print(script.group(0))
            s = template.replace("[place_holder]", script.group(0)).replace("[crontab_place_holder]", cron.group(0))
            output = open("./test/" + script.group(0).replace("js", "yml"), "w", encoding='utf-8')
            output.write(s)
            output.close()
finally:
    file.close()