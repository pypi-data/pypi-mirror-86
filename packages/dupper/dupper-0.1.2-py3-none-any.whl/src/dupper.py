# coding:utf-8
import os
import fire


class Dupper(object):
    """
    Dupper:                txtファイルの重複データをチェック・整理します\n

    dupper check:          txtファイルの重複データをチェックします\n
    """

    def check(self, name: str = None):
        """
        dupper check:          txtファイルの重複データをチェックします
        """
        if not name:
            print('ファイル名を"--name"オプションで指定してください')
            print('e.g. dupper check --name="./example.txt"')
            return

        if not os.path.isfile(name):
            print("{0}というファイルは存在しません".format(name))
            return

        records = self.get_records(name)
        cnt = len(records)
        print("全件数: {0}件、うち重複件数: {1}件"
              .format(cnt, cnt-len(self.uniq(records))))

    def get_records(self, name: str) -> list:
        records = []
        with open(name) as f:
            data = f.readlines()
            for text in data:
                text = text.replace('\n', '')
                records.append(text)

        return records

    def uniq(self, records: list) -> list:
        return list(set(records))


def main():
    fire.Fire(Dupper)
