import struct

import pymysql
import test


def testInt(value, mode):
    result = test.run(value, mode)
    return struct.unpack('i', result.get('plaintext').encode('utf-8'))[0]


def testString(value, mode):
    result = test.run(value, mode)
    return result


def simulate(mode):
    plaintext = 'My name is bob'
    result = testString(plaintext, mode)
    cipher = result['ciphertext']
    key = result['key']

    print('AES-128(', mode, ')')
    print('plaintext: ', result['plaintext'])
    print('ciphertext: ', cipher)
    print('key: ', key)
    print()

    conn = pymysql.connect(host='localhost', user='root', password='Dh1029Hj!@', db='paint', charset='utf8')
    cursor = conn.cursor()

    sql = 'INSERT into paint.test (data, datatype) values(%s, %s)'
    cursor.execute(sql, (cipher, 'cipher'))
    print('insert cipher : ' + cipher)
    print()

    sql = 'SELECT * FROM paint.test'
    cursor.execute(sql)
    result = cursor.fetchall()

    data = result[0][1].decode('utf-8')
    print('take data in MySQL : ', data)
    s = test.decrypt_message(key, data, mode)
    print('ciphertext to plaintext : ', s)

    conn.close()


if __name__ == '__main__':
    simulate('CBC') # change your mode if you want simulate
