package com.cnblog.clarck;

/**
 * 
 * 
 * @author clarck
 * 
 */
public class Facede {
	private SubSystemOne one;
	private SubSystemTwo two;
	private SubSystemThree three;
	private SubSystemFour four;

	public Facede() {
		one = new SubSystemOne();
		two = new SubSystemTwo();
		three = new SubSystemThree();
		four = new SubSystemFour();
	}

	public void methodA() {
		System.out.println("metodo a");
		one.methodOne();
		two.methodTwo();
		four.methodFour();
	}

	public void methodB() {
		System.out.println("metodo b");
		two.methodTwo();
		three.methodThree();
	}
}
