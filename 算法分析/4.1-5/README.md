./4.1-5/README.md

题目中介绍的思想，即"滑动窗口"的实现方法。
下面附上“滑动窗口实现寻找最大无重复的子串”的代码作为表示。

import static java.lang.Math.max;
 
public class lengthOfLongestSubstring {
    /***
     * 寻找最大无重复的子串，大小写敏感
     */
    static int  LongestSubstring(char[] s,int index){
        int []freq = new int [256];
        int l=0,r=-1;//[l,.....r]为滑动窗口；
        int res = 0;//返回值表示最长子串；
        //int temp = 0;//res的上一个值
//不需要，数组初始值就是0了
//        for(int i= 0;i<freq.length;i++){
//            freq[i]=0;
//        }
 
        while (l < s.length){//滑动窗口的终止条件!!!!!!
            if(r+1 < s.length && freq[s[r+1]] == 0){
                /***
                 * 滑动窗口一定注意判断条件必须有r+1<s.length()不然最后会越界
                 * freq[]表示256个char是否重复了
                 */
                r++;
                freq[s[r]]++;
            }
            else {
                /***
                 * 一定要注意这里的顺序，是先s[l]再l++,不然是不对的
                 * 会越界
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
        int index = 1;//表示最长子串开始位子的索引，从0开始
        int length = LongestSubstring(s, index);//length为最长子串的长度；
        System.out.println("length =" + length);
        System.out.println("start at" + index);
    }
}