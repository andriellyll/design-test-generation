class Solution {

    private static boolean isDigitOrLetter(char c) {
        return Character.isDigit(c) || Character.isLetter(c);
    }

    public static boolean isPalindrome(String s) {

        int i = 0;
        int j = s.length() - 1;

        char charAtI;
        char charAtJ;

        while (i <= ((s.length() - 1) / 2) && j > ((s.length() - 1) / 2)) {
            charAtI = s.charAt(i);
            charAtJ = s.charAt(j);

            if (isDigitOrLetter(charAtI) && isDigitOrLetter(charAtJ)) {
                System.out.println(charAtI);
                System.out.println(charAtJ);
                if (Character.toLowerCase(charAtI) == Character.toLowerCase(charAtJ)) {
                    i++;
                    j--;
                } else {
                    return false;
                }
            } else if (!isDigitOrLetter(charAtI)) {
                i++;
            } else if (!isDigitOrLetter(charAtJ)) {
                j--;
            }
        }

        return true;

    }

    public static void main(String[] args) {
        System.out.println(isPalindrome("A man, a plan, a canal: Panama"));
    }

}