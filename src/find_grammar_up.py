import os
from pathlib import Path
import resource
import subprocess
import sys
import threading

from run_selectx import main as run_selectx

POINTERS_FOLDER: str = "/mnt/data/MyOwnFolder/learning/p_algo/pointers"
FOLDER_WITH_GRAPHS : str = "/mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs"
FOLDER_WITH_BUILDER : str = "/mnt/data/MyOwnFolder/learning/p_algo/grammar_operations_cpp/build"

def set_memory_limit(max_memory_gb: int):
    """Устанавливает лимит памяти для текущего процесса"""
    max_memory_bytes = max_memory_gb * 1024 ** 3
    resource.setrlimit(resource.RLIMIT_AS, 
                      (max_memory_bytes, max_memory_bytes))

def run_with_memory_limit(command: list[str], max_memory_gb:int=12) -> bool:
    """
    Запускает процесс в отдельном потоке с ограничением памяти
    """
    run_with_memory_limit.result = False # type: ignore
    def target():
        try:
            set_memory_limit(max_memory_gb)
            subprocess.run(command, check=True, text=True, stdout=sys.stdout, stderr=sys.stderr)
            print("OK")
            run_with_memory_limit.result = True # type: ignore
        except MemoryError:
            print("Memory limit exceeded!")
        except subprocess.CalledProcessError as e:
            print(f"Process failed with code {e.returncode}")
        except Exception as e:
            print(f"Error: {e}")
    
    thread = threading.Thread(target=target)
    thread.start()
    thread.join()
    return run_with_memory_limit.result # type: ignore
    
def main():
    hi = 1_000_000_000
    lo = 10
    while hi - lo > 1:
        context_number = (hi + lo) // 2
        print(f"Context number {context_number}")
        with open(f"{POINTERS_FOLDER}/maximumContextNumber.txt", encoding='utf-8', mode='w') as file:
            file.write(f"{context_number}\n")
        subprocess.run([f"{POINTERS_FOLDER}/gradlew", "run"], check=True, text=True, cwd=POINTERS_FOLDER, stdout=sys.stdout, stderr=sys.stderr)
        run_selectx()
        graphs = Path(FOLDER_WITH_GRAPHS)
        success = True
        for graph in graphs.iterdir():
            if not run_with_memory_limit([f"{FOLDER_WITH_BUILDER}/grammarOperations", f"{graph}/slx_result.txt.ctxn", f"{graph}/grammar.cfg"]):
                print("Error")
                success = False
                break
        if success:
            lo = context_number
        else:
            hi = context_number
        print(f"There was {context_number}")
        with open("stat.txt", encoding='utf-8', mode='w') as file:
            file.write(f"{context_number}\n")

if __name__ == "__main__":
    main()
    
# 186 is ok for grammar

# Processing reactor...
#exceed: java.lang.invoke.LambdaMetafactory#metafactory(java.lang.invoke.MethodHandles$Lookup,java.lang.String,java.lang.invoke.MethodType,java.lang.invoke.MethodType,java.lang.invoke.MethodHandle,java.lang.invoke.MethodType):java.lang.invoke.CallSite
#exceed: java.lang.Integer#valueOf(int):java.lang.Integer
#exceed: reactor.test.StepVerifier#create(org.reactivestreams.Publisher):reactor.test.StepVerifier$FirstStep

# Processing org_apache_jackrabbit...
#exceed: java.lang.invoke.StringConcatFactory#makeConcatWithConstants(java.lang.invoke.MethodHandles$Lookup,java.lang.String,java.lang.invoke.MethodType,java.lang.String,java.lang.Object[]):java.lang.invoke.CallSite
#exceed: java.lang.String#valueOf(java.lang.Object):java.lang.String
#exceed: java.lang.StringBuilder#append(java.lang.String):java.lang.StringBuilder
#exceed: java.util.Iterator#next():java.lang.Object
#exceed: java.util.Iterator#hasNext():boolean
#exceed: org.slf4j.Logger#debug(java.lang.String):void
#exceed: java.lang.Object#<init>():void
#exceed: org.apache.jackrabbit.core.state.NodeState#getNodeId():org.apache.jackrabbit.core.id.NodeId
#exceed: java.lang.String#equals(java.lang.Object):boolean
#exceed: java.util.Map#put(java.lang.Object,java.lang.Object):java.lang.Object
#exceed: java.util.Map#get(java.lang.Object):java.lang.Object
#exceed: java.lang.Object#equals(java.lang.Object):boolean
#exceed: java.util.ArrayList#add(java.lang.Object):boolean
#exceed: org.slf4j.LoggerFactory#getLogger(java.lang.Class):org.slf4j.Logger
#exceed: java.util.ArrayList#<init>():void
#exceed: javax.jcr.RepositoryException#<init>(java.lang.String,java.lang.Throwable):void
#exceed: java.util.Set#iterator():java.util.Iterator
#exceed: java.util.List#iterator():java.util.Iterator
#exceed: javax.jcr.Session#save():void
#exceed: java.util.List#add(java.lang.Object):boolean
#exceed: javax.jcr.Node#addNode(java.lang.String):javax.jcr.Node
#exceed: java.lang.System#currentTimeMillis():long
#exceed: org.slf4j.Logger#error(java.lang.String,java.lang.Throwable):void
#exceed: javax.jcr.Session#logout():void
#exceed: java.lang.StringBuffer#append(java.lang.String):java.lang.StringBuffer
#exceed: javax.jcr.Node#getPath():java.lang.String
#exceed: javax.jcr.Node#setProperty(java.lang.String,java.lang.String):javax.jcr.Property
#exceed: java.lang.Integer#valueOf(int):java.lang.Integer
#exceed: javax.jcr.Session#getWorkspace():javax.jcr.Workspace
#exceed: java.util.List#size():int
#exceed: javax.jcr.query.Query#execute():javax.jcr.query.QueryResult
#exceed: org.apache.jackrabbit.core.query.AbstractQueryTest#executeXPathQuery(java.lang.String,javax.jcr.Node[]):void
#exceed: java.lang.Object#toString():java.lang.String
#exceed: javax.jcr.Node#addNode(java.lang.String,java.lang.String):javax.jcr.Node
#exceed: java.util.HashMap#put(java.lang.Object,java.lang.Object):java.lang.Object
#exceed: java.lang.Boolean#valueOf(boolean):java.lang.Boolean
#exceed: java.util.HashMap#<init>():void
#exceed: org.apache.jackrabbit.api.security.user.AbstractUserTest#save(javax.jcr.Session):void
#exceed: java.security.Principal#getName():java.lang.String
#exceed: javax.jcr.Node#addMixin(java.lang.String):void
#exceed: javax.jcr.Node#getNode(java.lang.String):javax.jcr.Node
#exceed: javax.jcr.Node#save():void
#exceed: javax.jcr.Node#remove():void
#exceed: org.apache.jackrabbit.test.AbstractJCRTest#getHelper():org.apache.jackrabbit.test.RepositoryHelper
#exceed: java.lang.Long#valueOf(long):java.lang.Long
#exceed: java.lang.String#length():int
#exceed: java.util.HashSet#add(java.lang.Object):boolean
#exceed: javax.jcr.RepositoryException#<init>(java.lang.String):void
#exceed: java.util.ArrayList#size():int
#exceed: java.util.Arrays#fill(byte[],int,int,byte):void
#exceed: javax.jcr.Node#getSession():javax.jcr.Session

# Processing com_fasterxml_jackson...
#exceed: java.util.Arrays#asList(java.lang.Object[]):java.util.List
#exceed: javax.jcr.Node#getProperty(java.lang.String):javax.jcr.Property
#exceed: javax.jcr.Value#getString():java.lang.String
#exceed: javax.jcr.Session#getValueFactory():javax.jcr.ValueFactory
#exceed: javax.jcr.nodetype.PropertyDefinition#getName():java.lang.String
#exceed: org.apache.jackrabbit.test.NotExecutableException#<init>(java.lang.String):void
#exceed: javax.jcr.query.QueryManager#createQuery(java.lang.String,java.lang.String):javax.jcr.query.Query
#exceed: junit.framework.TestSuite#addTestSuite(java.lang.Class):void
#exceed: javax.jcr.NodeIterator#nextNode():javax.jcr.Node
#exceed: javax.jcr.Session#getRootNode():javax.jcr.Node
#exceed: org.apache.jackrabbit.test.AbstractJCRTest#<init>():void
#exceed: javax.jcr.Session#getItem(java.lang.String):javax.jcr.Item
#exceed: javax.jcr.NodeIterator#hasNext():boolean
#exceed: javax.jcr.Node#getName():java.lang.String
#exceed: org.apache.jackrabbit.test.AbstractJCRTest#ensureMixinType(javax.jcr.Node,java.lang.String):void
#exceed: javax.jcr.Node#checkin():javax.jcr.version.Version
#exceed: javax.jcr.version.VersionManager#checkin(java.lang.String):javax.jcr.version.Version
#exceed: javax.jcr.Workspace#getName():java.lang.String
#exceed: org.slf4j.Logger#warn(java.lang.String):void
#exceed: java.io.ByteArrayInputStream#<init>(byte[]):void
#exceed: java.lang.IllegalStateException#<init>(java.lang.String):void
#exceed: java.lang.IllegalArgumentException#<init>(java.lang.String):void
#exceed: org.apache.jackrabbit.spi.NameFactory#create(java.lang.String,java.lang.String):org.apache.jackrabbit.spi.Name
#exceed: java.util.HashSet#<init>():void
#exceed: java.lang.String#substring(int,int):java.lang.String
#exceed: java.lang.StringBuffer#toString():java.lang.String
#exceed: org.apache.jackrabbit.spi.commons.query.xpath.JJTXPathState#closeNodeScope(org.apache.jackrabbit.spi.commons.query.xpath.Node,boolean):void
#exceed: org.apache.jackrabbit.spi.commons.query.xpath.XPath#jj_consume_token(int):org.apache.jackrabbit.spi.commons.query.xpath.Token
#exceed: org.apache.jackrabbit.spi.commons.query.xpath.SimpleNode#<init>(org.apache.jackrabbit.spi.commons.query.xpath.XPath,int):void
#exceed: org.apache.jackrabbit.spi.commons.query.xpath.JJTXPathState#openNodeScope(org.apache.jackrabbit.spi.commons.query.xpath.Node):void
#exceed: org.apache.jackrabbit.spi.commons.query.xpath.SimpleNode#processToken(org.apache.jackrabbit.spi.commons.query.xpath.Token):void
#exceed: org.apache.jackrabbit.spi.commons.query.xpath.XPathTokenManager#jjCheckNAdd(int):void
#exceed: org.apache.jackrabbit.spi.commons.query.xpath.XPathTokenManager#jjCheckNAddTwoStates(int,int):void
#exceed: org.apache.jackrabbit.spi.commons.query.xpath.XPathTokenManager#jjAddStates(int,int):void
#exceed: java.io.InputStream#close():void
#exceed: java.lang.StringBuilder#append(java.lang.String):java.lang.StringBuilder
#exceed: java.lang.StringBuilder#toString():java.lang.String
#exceed: java.lang.StringBuilder#<init>():void
#exceed: java.lang.Object#<init>():void
#exceed: java.lang.Object#getClass():java.lang.Class
#exceed: java.lang.String#format(java.lang.String,java.lang.Object[]):java.lang.String
#exceed: com.fasterxml.jackson.core.JsonParser#nextToken():com.fasterxml.jackson.core.JsonToken
#exceed: java.lang.Enum#ordinal():int
#exceed: java.lang.Class#getName():java.lang.String
#exceed: com.fasterxml.jackson.databind.JavaType#getRawClass():java.lang.Class
#exceed: java.util.Iterator#next():java.lang.Object
#exceed: java.util.Iterator#hasNext():boolean
#exceed: java.lang.String#length():int
#exceed: java.lang.Integer#valueOf(int):java.lang.Integer
#exceed: java.lang.IllegalArgumentException#<init>(java.lang.String):void
#exceed: java.util.HashSet#add(java.lang.Object):boolean
#exceed: java.lang.Class#isAssignableFrom(java.lang.Class):boolean
#exceed: java.util.Map#put(java.lang.Object,java.lang.Object):java.lang.Object
#exceed: java.util.HashMap#put(java.lang.Object,java.lang.Object):java.lang.Object
#exceed: java.lang.StringBuilder#append(char):java.lang.StringBuilder
#exceed: java.lang.String#equals(java.lang.Object):boolean
#exceed: java.lang.String#charAt(int):char

# Processing org_jivesoftware_openfire...
#exceed: javax.servlet.jsp.JspWriter#write(java.lang.String):void
#exceed: javax.servlet.jsp.PageContext#getOut():javax.servlet.jsp.JspWriter
#exceed: org.apache.jasper.runtime.TagHandlerPool#get(java.lang.Class):javax.servlet.jsp.tagext.Tag
#exceed: org.apache.jasper.runtime.TagHandlerPool#reuse(javax.servlet.jsp.tagext.Tag):void
#exceed: org.apache.taglibs.standard.tag.rt.fmt.MessageTag#setPageContext(javax.servlet.jsp.PageContext):void
#exceed: org.apache.taglibs.standard.tag.rt.fmt.MessageTag#setParent(javax.servlet.jsp.tagext.Tag):void
#exceed: org.apache.taglibs.standard.tag.rt.fmt.MessageTag#setKey(java.lang.String):void
#exceed: org.apache.taglibs.standard.tag.rt.fmt.MessageTag#doStartTag():int
#exceed: org.apache.taglibs.standard.tag.rt.fmt.MessageTag#doEndTag():int
#exceed: javax.servlet.jsp.JspFactory#releasePageContext(javax.servlet.jsp.PageContext):void
#exceed: org.apache.jasper.runtime.PageContextImpl#proprietaryEvaluate(java.lang.String,java.lang.Class,javax.servlet.jsp.PageContext,org.apache.jasper.runtime.ProtectedFunctionMapper):java.lang.Object
#exceed: javax.servlet.jsp.SkipPageException#<init>():void
#exceed: java.util.Set#add(java.lang.Object):boolean
#exceed: javax.servlet.jsp.JspWriter#write(int):void
#exceed: javax.servlet.jsp.tagext.TagAdapter#<init>(javax.servlet.jsp.tagext.SimpleTag):void
#exceed: org.apache.taglibs.standard.tag.rt.core.ForEachTag#doFinally():void
#exceed: java.lang.Boolean#booleanValue():boolean
#exceed: org.apache.jasper.runtime.TagHandlerPool#getTagHandlerPool(javax.servlet.ServletConfig):org.apache.jasper.runtime.TagHandlerPool
#exceed: org.apache.jasper.runtime.TagHandlerPool#release():void
#exceed: java.lang.String#equals(java.lang.Object):boolean
#exceed: javax.servlet.jsp.JspWriter#print(java.lang.String):void
#exceed: javax.servlet.jsp.PageContext#setAttribute(java.lang.String,java.lang.Object):void
#exceed: org.apache.tomcat.InstanceManager#destroyInstance(java.lang.Object):void
#exceed: java.lang.invoke.StringConcatFactory#makeConcatWithConstants(java.lang.invoke.MethodHandles$Lookup,java.lang.String,java.lang.invoke.MethodType,java.lang.String,java.lang.Object[]):java.lang.invoke.CallSite
#exceed: org.jivesoftware.util.ParamUtils#getParameter(javax.servlet.http.HttpServletRequest,java.lang.String):java.lang.String
#exceed: java.util.HashMap#put(java.lang.Object,java.lang.Object):java.lang.Object
#exceed: org.apache.taglibs.standard.tag.rt.core.IfTag#setPageContext(javax.servlet.jsp.PageContext):void
#exceed: org.apache.taglibs.standard.tag.rt.core.IfTag#setParent(javax.servlet.jsp.tagext.Tag):void
#exceed: org.apache.taglibs.standard.tag.rt.core.IfTag#setTest(boolean):void
#exceed: org.apache.taglibs.standard.tag.rt.core.IfTag#doStartTag():int
#exceed: org.apache.taglibs.standard.tag.rt.core.IfTag#doAfterBody():int
#exceed: org.apache.taglibs.standard.tag.rt.core.IfTag#doEndTag():int
#exceed: org.apache.taglibs.standard.tag.rt.core.OutTag#setPageContext(javax.servlet.jsp.PageContext):void
#exceed: org.apache.taglibs.standard.tag.rt.core.OutTag#setParent(javax.servlet.jsp.tagext.Tag):void
#exceed: org.apache.taglibs.standard.tag.rt.core.OutTag#setValue(java.lang.Object):void
#exceed: org.apache.taglibs.standard.tag.rt.core.OutTag#doStartTag():int
#exceed: org.apache.taglibs.standard.tag.rt.core.OutTag#doEndTag():int
#exceed: javax.servlet.jsp.PageContext#getELContext():javax.el.ELContext
#exceed: org.apache.taglibs.standard.tag.rt.core.WhenTag#setPageContext(javax.servlet.jsp.PageContext):void
#exceed: org.apache.taglibs.standard.tag.rt.core.WhenTag#setParent(javax.servlet.jsp.tagext.Tag):void
#exceed: org.apache.taglibs.standard.tag.rt.core.WhenTag#setTest(boolean):void
#exceed: org.apache.taglibs.standard.tag.rt.core.WhenTag#doStartTag():int
#exceed: org.apache.taglibs.standard.tag.rt.core.WhenTag#doAfterBody():int
#exceed: org.apache.taglibs.standard.tag.rt.core.WhenTag#doEndTag():int
#exceed: javax.servlet.jsp.PageContext#popBody():javax.servlet.jsp.JspWriter
#exceed: org.apache.jasper.el.JspValueExpression#<init>(java.lang.String,javax.el.ValueExpression):void
#exceed: org.apache.jasper.el.JspValueExpression#getValue(javax.el.ELContext):java.lang.Object
#exceed: javax.servlet.http.HttpServletResponse#setHeader(java.lang.String,java.lang.String):void
#exceed: java.util.LinkedHashSet#<init>(int):void
#exceed: org.apache.tomcat.InstanceManager#newInstance(java.lang.Object):void
#exceed: org.apache.taglibs.standard.tag.common.core.ChooseTag#setPageContext(javax.servlet.jsp.PageContext):void
#exceed: org.apache.taglibs.standard.tag.common.core.ChooseTag#setParent(javax.servlet.jsp.tagext.Tag):void
#exceed: org.apache.taglibs.standard.tag.common.core.ChooseTag#doStartTag():int
#exceed: org.apache.taglibs.standard.tag.common.core.ChooseTag#doAfterBody():int
#exceed: org.apache.taglibs.standard.tag.common.core.ChooseTag#doEndTag():int
#exceed: javax.el.ExpressionFactory#createValueExpression(javax.el.ELContext,java.lang.String,java.lang.Class):javax.el.ValueExpression
#exceed: javax.servlet.jsp.JspContext#getELContext():javax.el.ELContext
#exceed: javax.servlet.http.HttpServletResponse#sendRedirect(java.lang.String):void
#exceed: javax.servlet.http.HttpServletRequest#getParameter(java.lang.String):java.lang.String
#exceed: java.util.Map#put(java.lang.Object,java.lang.Object):java.lang.Object
#exceed: org.jivesoftware.util.LocaleUtils#getLocalizedString(java.lang.String,java.util.Locale):java.lang.String
#exceed: java.util.Iterator#next():java.lang.Object
#exceed: java.util.Iterator#hasNext():boolean
#exceed: org.jivesoftware.openfire.XMPPServer#getInstance():org.jivesoftware.openfire.XMPPServer
#exceed: java.util.Map#get(java.lang.Object):java.lang.Object
#exceed: org.dom4j.Element#addAttribute(java.lang.String,java.lang.String):org.dom4j.Element
#exceed: java.lang.Boolean#valueOf(boolean):java.lang.Boolean
#exceed: java.lang.invoke.LambdaMetafactory#metafactory(java.lang.invoke.MethodHandles$Lookup,java.lang.String,java.lang.invoke.MethodType,java.lang.invoke.MethodType,java.lang.invoke.MethodHandle,java.lang.invoke.MethodType):java.lang.invoke.CallSite
#exceed: org.xmpp.forms.FormField#setVariable(java.lang.String):void
#exceed: java.lang.Object#<init>():void
#exceed: java.lang.String#trim():java.lang.String
#exceed: java.lang.StringBuilder#append(java.lang.String):java.lang.StringBuilder
#exceed: java.lang.String#isEmpty():boolean
#exceed: org.jivesoftware.util.cache.ExternalizableUtil#getInstance():org.jivesoftware.util.cache.ExternalizableUtil
#exceed: java.lang.String#valueOf(java.lang.Object):java.lang.String
#exceed: java.util.List#iterator():java.util.Iterator
#exceed: org.slf4j.Logger#error(java.lang.String,java.lang.Throwable):void
#exceed: org.jivesoftware.openfire.muc.MUCRoom#getJID():org.xmpp.packet.JID
#exceed: org.xmpp.forms.FormField#setType(org.xmpp.forms.FormField$Type):void
#exceed: org.xmpp.forms.DataForm#addField():org.xmpp.forms.FormField
#exceed: org.slf4j.Logger#debug(java.lang.String):void
#exceed: java.lang.Long#valueOf(long):java.lang.Long
#exceed: org.jivesoftware.util.SystemProperty#getValue():java.lang.Object
#exceed: org.xmpp.forms.FormField#addValue(java.lang.Object):void
#exceed: java.lang.Integer#valueOf(int):java.lang.Integer
#exceed: org.slf4j.Logger#debug(java.lang.String,java.lang.Object):void
#exceed: java.util.Collection#iterator():java.util.Iterator
#exceed: java.util.ArrayList#add(java.lang.Object):boolean
#exceed: org.slf4j.Logger#debug(java.lang.String,java.lang.Object,java.lang.Object):void
#exceed: org.jivesoftware.util.LocaleUtils#getLocalizedString(java.lang.String):java.lang.String
#exceed: org.slf4j.LoggerFactory#getLogger(java.lang.Class):org.slf4j.Logger
#exceed: java.util.ArrayList#<init>():void
#exceed: java.sql.PreparedStatement#setString(int,java.lang.String):void
#exceed: org.slf4j.Logger#trace(java.lang.String,java.lang.Object):void
#exceed: org.xmpp.forms.FormField#setLabel(java.lang.String):void
#exceed: org.dom4j.Element#addElement(java.lang.String):org.dom4j.Element
#exceed: org.jivesoftware.openfire.SessionManager#getInstance():org.jivesoftware.openfire.SessionManager
#exceed: org.dom4j.Element#attributeValue(java.lang.String):java.lang.String
#exceed: org.xmpp.packet.JID#toString():java.lang.String
#exceed: org.xmpp.packet.JID#getNode():java.lang.String
#exceed: java.util.Collection#stream():java.util.stream.Stream
#exceed: org.dom4j.Element#setText(java.lang.String):void
#exceed: org.dom4j.Element#element(java.lang.String):org.dom4j.Element
#exceed: org.jivesoftware.database.DbConnectionManager#closeConnection(java.sql.ResultSet,java.sql.Statement,java.sql.Connection):void
#exceed: java.util.Set#iterator():java.util.Iterator
#exceed: org.jivesoftware.database.DbConnectionManager#closeConnection(java.sql.Statement,java.sql.Connection):void
#exceed: java.sql.Connection#prepareStatement(java.lang.String):java.sql.PreparedStatement
#exceed: org.jivesoftware.util.SystemProperty$Builder#ofType(java.lang.Class):org.jivesoftware.util.SystemProperty$Builder
#exceed: org.jivesoftware.util.SystemProperty$Builder#setKey(java.lang.String):org.jivesoftware.util.SystemProperty$Builder
#exceed: org.jivesoftware.util.SystemProperty$Builder#setDynamic(boolean):org.jivesoftware.util.SystemProperty$Builder
#exceed: java.lang.Throwable#getMessage():java.lang.String
#exceed: java.util.Map#remove(java.lang.Object):java.lang.Object
#exceed: java.util.concurrent.locks.Lock#unlock():void
#exceed: org.jivesoftware.util.SystemProperty$Builder#build():org.jivesoftware.util.SystemProperty

