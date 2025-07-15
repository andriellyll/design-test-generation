package com.cnblog.clarck;

/**
 * 
 * 
 * @author clarck
 * 
 */
public class Director {
	public void Construct(Builder builder) {
		builder.buildPartA();
		builder.buildPartB();
	}
}
