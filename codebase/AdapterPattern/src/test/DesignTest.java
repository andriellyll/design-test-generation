package test;

import static org.junit.Assert.*;
import org.junit.Test;

import org.junit.Before;
import org.junit.Ignore;

import java.util.Set;

import org.designwizard.api.DesignWizard;
import org.designwizard.design.ClassNode;
import org.designwizard.design.Design;
import org.designwizard.design.MethodNode;
import org.designwizard.design.FieldNode;
import org.designwizard.design.PackageNode;
import org.designwizard.design.Modifier;

public class DesignTest {
    @Test
    public void testClientDoesNotInstantiateAdaptee() throws Exception {
        // Always instantiate DesignWizard exactly like this
        DesignWizard dw = new DesignWizard("bin");
        ClassNode clientClass = dw.getClass("com.cnblog.clarck.Client");
        ClassNode adapteeClass = dw.getClass("com.cnblog.clarck.Adaptee");

        Set<ClassNode> calleeClasses = clientClass.getCalleeClasses();

        assertFalse(calleeClasses.contains(adapteeClass));
    }
}
