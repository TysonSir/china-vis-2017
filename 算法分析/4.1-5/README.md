./4.1-5/README.md

��Ŀ�н��ܵ�˼�룬��"��������"��ʵ�ַ�����
���渽�ϡ���������ʵ��Ѱ��������ظ����Ӵ����Ĵ�����Ϊ��ʾ��

import static java.lang.Math.max;
 
public class lengthOfLongestSubstring {
    /***
     * Ѱ��������ظ����Ӵ�����Сд����
     */
    static int  LongestSubstring(char[] s,int index){
        int []freq = new int [256];
        int l=0,r=-1;//[l,.....r]Ϊ�������ڣ�
        int res = 0;//����ֵ��ʾ��Ӵ���
        //int temp = 0;//res����һ��ֵ
//����Ҫ�������ʼֵ����0��
//        for(int i= 0;i<freq.length;i++){
//            freq[i]=0;
//        }
 
        while (l < s.length){//�������ڵ���ֹ����!!!!!!
            if(r+1 < s.length && freq[s[r+1]] == 0){
                /***
                 * ��������һ��ע���ж�����������r+1<s.length()��Ȼ����Խ��
                 * freq[]��ʾ256��char�Ƿ��ظ���
                 */
                r++;
                freq[s[r]]++;
            }
            else {
                /***
                 * һ��Ҫע�������˳������s[l]��l++,��Ȼ�ǲ��Ե�
                 * ��Խ��
                 */
                freq[s[l]]--;
                l++;
            }
            res = max(res,r-l+1);

        }
        System.out.println(index);
        return res;
    }
 
    public static void main(String[] args) {
        char[] s = {'a', ' ', '!', 'b', 'a', 'c', 'b'};
        int index = 1;//��ʾ��Ӵ���ʼλ�ӵ���������0��ʼ
        int length = LongestSubstring(s, index);//lengthΪ��Ӵ��ĳ��ȣ�
        System.out.println("length =" + length);
        System.out.println("start at" + index);
    }
}