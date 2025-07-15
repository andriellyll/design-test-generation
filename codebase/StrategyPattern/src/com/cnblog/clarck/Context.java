package com.cnblog.clarck;

/**
 * 上下文
 * 
 * @author clarck
 * 
 */
public class Context {
	Strategy mStrategy;

	public Context(Strategy strategy) {
		mStrategy = strategy;
	}

	public void ContextInterface() {
		mStrategy.algorithmInterface();
	}
}
